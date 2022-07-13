# oci-load-file-into-adw-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#
import io
import os
import oci
import json
import datetime
import logging

from fdk import response

class devops:
    def __init__(self,region):
        self.region = region
        self.signer = oci.auth.signers.get_resource_principals_signer()


    def invoke_deployment(self, image_version, oci_deployment_pipeline_id):
        try:
            devops_client = oci.devops.DevopsClient(config={'region': self.region}, signer = self.signer)
            deployment_timestamp = datetime.datetime.now().isoformat()
            logging.getLogger().info('Initialized devops client')
            create_deployment_response = devops_client.create_deployment(
                create_deployment_details=oci.devops.models.CreateDeployPipelineDeploymentDetails(
                    deployment_type="PIPELINE_DEPLOYMENT",
                    deploy_pipeline_id=oci_deployment_pipeline_id,
                    display_name=f"deployment_{deployment_timestamp}",
                    deployment_arguments=oci.devops.models.DeploymentArgumentCollection(
                        items=[
                            oci.devops.models.DeploymentArgument(
                                name="BUILDRUN_HASH",
                                value=image_version)]))
            )
            # Get the data from response
            logging.getLogger().info('Response ' + str(create_deployment_response.data))
            return create_deployment_response

        except Exception as error:
            logging.getLogger().error("Deployment Exception" + str(error))

def handler(ctx, data: io.BytesIO=None):
    try:
        input = json.loads(data.getvalue())
        image_version = input[0]['data']['request']['path'].split('/')[-1]
        image_digest = input[0]['data']['additionalDetails']['digest']
        logging.getLogger().info(f"New image version is {image_version} and image digest is {image_digest}")
        oci_region = os.environ['oci_region']
        oci_deployment_pipeline_id = os.environ['oci_deployment_pipeline_id']
        devops_handler = devops(oci_region)
        create_deployment_response = devops_handler.invoke_deployment(image_version,oci_deployment_pipeline_id)
        return response.Response(
            ctx,
            response_data=json.dumps({"status": f"{create_deployment_response}"}),
            headers={"Content-Type": "application/json"})
    except Exception as error:
        logging.getLogger().error("Exception" + str(error))

