# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import os
import json
import logging
import subprocess

import oci

from fdk import response

def execute_shell_command(cmd):
    try:
        return (subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8'))

    except Exception as error:
        logging.getLogger().info(f'Exception while executing  shell commands - str({error})')
   

class oci_cli_actions():
    def __init__(self,region,signer):
        """Init with  a region and resource principal signer"""
        self.region = region
        self.signer = signer

    def download_artifact(self,artifact_repo_id,artifact_path,artifact_version):
        try:
            logging.getLogger().info("Downloading the artifact")
            oci_artifact_client = oci.generic_artifacts_content.GenericArtifactsContentClient(config={'region': self.region}, signer = self.signer)
            get_generic_artifact_content_by_path_response = oci_artifact_client.get_generic_artifact_content_by_path(
                repository_id=artifact_repo_id,
                artifact_path=artifact_path,
                version=artifact_version
            )
            logging.getLogger().info(f"attemtping to write to path /tmp/{artifact_path}")
            with open(f'/tmp/{artifact_path}', 'wb') as target_file:
                for chunk in get_generic_artifact_content_by_path_response.data.raw.stream(1024 * 1024, decode_content=False):
                    target_file.write(chunk)
            outcome = execute_shell_command(['ls','-ltrh','/tmp/'])
            logging.getLogger().info("Temp file information " + str(outcome))
        
        except Exception as error:
            logging.getLogger().info(f'Exception while downloading artifact - {error}')

    
    def oke_deployment(self,oke_cluster_id,artifact_path,artifact_version):
        try:
            ce_client = oci.container_engine.ContainerEngineClient(config={'region': self.region}, signer=self.signer)
            config_response = ce_client.create_kubeconfig(oke_cluster_id)
            config_path="/tmp/kubeconfig"
            with open(config_path, 'w') as file:
                file.write(config_response.data.text)
            os.environ['KUBECONFIG'] = config_path
            outcome = execute_shell_command(['chmod','go-r',config_path])
            chart_name = artifact_path.strip('.zip').replace("_","-")
            logging.getLogger().info(f"Attempting Helm install with version {artifact_version}")
            outcome = execute_shell_command(['helm','history',chart_name])
            logging.getLogger().info("helm current history - " + str(outcome))
            outcome = execute_shell_command(['helm','upgrade','--install',chart_name,f'/tmp/{artifact_path}'])
            outcome = execute_shell_command(['helm','history',chart_name])
            logging.getLogger().info("helm post deployment history - " + str(outcome))

        except Exception as error:
            logging.getLogger().info(f'Exception while deploying to OKE - {error}')
        


def handler(ctx, data: io.BytesIO=None):
    try:
        body = json.loads(data.getvalue()) 
        logging.getLogger().info("Fetching the information")
        artifact_repo_id = body[0]['data']['stateChange']['current']['repositoryId']
        artifact_path = body[0]['data']['stateChange']['current']['artifactPath']
        artifact_version = body[0]['data']['stateChange']['current']['version']
        region = os.environ['oci_region']
        oke_cluster_id = os.environ['oke_cluster_id']
        signer = oci.auth.signers.get_resource_principals_signer()
        os.environ['OCI_CLI_AUTH']="resource_principal" #set OCI CLI to use resource_principal authorization
        logging.getLogger().info(f'Input Params Repo = {artifact_repo_id} Path = {artifact_path}, Version = {artifact_version}')
        artifact_handler = oci_cli_actions(region,signer)
        artifact_handler.download_artifact(artifact_repo_id,artifact_path,artifact_version)
        artifact_handler.oke_deployment(oke_cluster_id,artifact_path,artifact_version)
        logging.getLogger().info(artifact_handler)
        return response.Response(
            ctx, 
            response_data=json.dumps({"status": "Hello World! with customImage"}),
            headers={"Content-Type": "application/json"})
    except Exception as error:
        logging.getLogger().info(f'Exception - {error}')
        return response.Response(
            ctx, 
            response_data=json.dumps({"status": f'Exception - str({error})'}),
            headers={"Content-Type": "application/json"})