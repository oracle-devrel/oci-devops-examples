Sample illustration of OCI DevOps deployment pipeline with *DevOps Deploy Shell stage*
------------

## Deploy Shell Stage
The shell stage allows you to run custom commands in the deployment pipeline. This stage can be added at any point in the deployment pipeline. You must prepare a command specification YAML file containing all the steps that you want to run during the deployment. The command spec is run on a container instance host in the selected compartment and subnet in your tenancy.

## Key benefits of adding a Shell stage:

- Automate deployments to OCI platforms such as service mesh and container instances using OCI CLI and other pre-installed tools.

- OCI CLI is pre-authenticated to use the pipeline resource principal to access OCI resources.

- Run a database schema migration using command line tools such as Oracle SQL Developer Command Line (SQLcl).

- Use any pipeline parameters by referencing them in the spec. Also, replace parameters and variables during the deployment run.

- Perform integration tests on artifacts before deploying to production.

- Customize the DevOps workflow. For example, you can wait for some resources to be ready before the pipeline deploys additional resources.

Specific instructions to download only this sample.
---

```
    $ git init oci-deployment-shell-stages
    $ cd oci-deployment-shell-stages
    $ git remote add origin https://github.com/oracle-devrel/oci-devops-examples
    $ git config core. sparsecheckout true
    $ echo "oci-deployment-examples/ooci-deployment-shell-stages/*">>.git/info/sparse-checkout
    $ git pull --depth=1 origin main
```


## Sample 1 . Simple Shell stage execution.

### Network requirement.

- A valid OCI Virtual cloud network (OCI VCN) with at least one subnet.
- The subnet will be used by the container instances to run the shell stage executions.

### OCI Identity setup

- Create a dynamic group with the below rule.

```java
ALL {resource.type = 'devopsdeploypipeline', resource.compartment.id = 'COMPARTMENT_OCID'}
```

- Create a dynamic policy with the below statements.

```java
Allow dynamic-group  <NAME OF THE DYNAMIC GROUP> to manage virtual-network-family in compartment <NAME OF THE COMPARTMENT> 
Allow dynamic-group <NAME OF THE DYNAMIC GROUP>  to manage ons-topics in compartment <NAME OF THE COMPARTMENT>
Allow dynamic-group <NAME OF THE DYNAMIC GROUP>  to manage all-artifacts in compartment <NAME OF THE COMPARTMENT> 
```

### OCI DevOps setup

- Create an `OCI Notification topic` - https://docs.oracle.com/en-us/iaas/Content/Notification/Tasks/create-topic.htm#top
- Create a DevOps project and associate it with the topic. Ensure to enable logs for the DevOps project.

![](images/oci-devops-logs.png)

- Create a new DevOps artifact of type `command spec`

![](images/oci-devops-artifact.png)

- Use option `inline` as the source type. Copy the values from file [shellstage-simple. yaml](yamls/shellstage-simple.yaml) and paste them to the artifact values field. Enable the option `Allow parameterization` and click `Add`.

![](images/oci-inline-artifacts.png)

- Create a `deployment pipeline`.

![](images/oci-deployment-pipeline.png)

- Use `+` and add a deployment stage of type `Execute managed shell command`.

![](images/oci-exec-shell-stage.png)

- Provide a name and select the `DevOps artifact` created.

![](images/oci-artifact-for-stage.png)

- Select a desired container instance configuration, for this sample we will use the default values.

![](images/oci-container-instance-sample.png)

- Select network configuration as applicable.

![](images/oci-vcn-info.png)

- Click `Add`.

![](images/oci-deploy-stages.png)

- Click `Run pipeline` and wait for the stages to complete.

![](images/oci-shell-simple-op.png)

- The simple stage will display a `hello` message.

## Sample 2. Multiple deploy shell stages.

### Requirement.

- We are using an OKE (Oracle Cloud Infrastructure Container Engine for Kubernetes ) resource lifecycle for this sample, so you need to have an OKE for this sample.
- The sample made using public Kubernetes references using NGINX ensure that the OKE can reach the public network. If not you may adjust the inputArtifact URL value accordingly.

### OCI Identity setup

- Create a dynamic group with the below rule.

```java
ALL {resource.type = 'devopsdeploypipeline', resource.compartment.id = 'COMPARTMENT_OCID'}
```

- Create a dynamic policy with the below statements.

```java
Allow dynamic-group  <NAME OF THE DYNAMIC GROUP> to manage virtual-network-family in compartment <NAME OF THE COMPARTMENT> 
Allow dynamic-group <NAME OF THE DYNAMIC GROUP>  to manage ons-topics in compartment <NAME OF THE COMPARTMENT>
Allow dynamic-group <NAME OF THE DYNAMIC GROUP>  to manage all-artifacts in compartment <NAME OF THE COMPARTMENT>
Allow dynamic-group <NAME OF THE DYNAMIC GROUP>  to manage cluster-family in compartment <NAME OF THE COMPARTMENT> 
```


### OCI Artifact registry.

- Create an `OCI Artifact registry repo` - https://docs.oracle.com/en-us/iaas/Content/artifacts/create-repo.htm#create-repo

![](images/oci-artifact-repo.png)

- Upload file [shellstage-oke-deploy.yaml](yamls/shellstage-oke-deploy.yaml) to the repo as an artifact.

![](images/oci-artifact-deploy.png)


- Upload file [shellstage-oke-delete.yaml](yamls/shellstage-oke-delete.yaml) to the repo as an artifact.

![](images/oci-kube-delete.png)

![](images/oci-all-artifacts.png)


### OCI DevOps setup

- Create an `OCI Notification topic` - https://docs.oracle.com/en-us/iaas/Content/Notification/Tasks/create-topic.htm#top
- Create a DevOps project and associate it with the topic. Ensure to enable logs for the DevOps project. Or you may reuse the one created for the previous sample.

![](images/oci-devops-logs.png)

- Add a DevOps artifact of type `command spec` with `Artifact registry repository as source`

- Select the artifact repo created.

![](images/oci-devops-artifact-1.png)

- Use `Select existing location` and select the `oke-deploy` artifact. Click `Add` to add the artifact.

![](images/oci-oke-deploy-artifact-devops.png)

- Add another DevOps artifact of type `Command spec`. Use `Artifact registry repository` as the source. Select the `Artifact registry repo` created.

![](images/oci-devops-artifact-delete-1.png)

- Select `Existing Location` and select `oke-delete. yaml` artifact from the repo. Click `Add` and add the artifact.

![](images/oci-oke-delete-devops-artifact.png)

![](images/oci-artifact-devops-all.png)

- Create a deployment pipeline.

![](images/oci-deploy-pipeline.png)

- Use '+' with in the pipeline and add a deployment stage of type `Execute managed shell command`.

![](images/oci-exec-shell-stage.png)

- Provide a name for the stage and associate it with the artifact for `oke deploy`.

![](images/oci-ss-oke-deploy-1.png)

- Keep the default configuration for the `Container instance` specification.

- Select a network configuration from which it can reach the OKE Cluster endpoint. We are using the node subnet of OKE for this sample.

- Click `Add` and add the stage.

- In this sample, we will be provisioning a resource on to OKE namespace and after the verification, will be deleting it. So to have a confirmation before deletion, we will be adding an `Approval stage here`.

- Use `+` and add a stage of type `Approval`.

![](images/oci-approval-stage.png)

- Provide a name for the stage and click `Add`

![](images/oci-approval-stage-2.png)

![](images/oci-approval-stage-3.png)

- Click `+` and add another deployment stage of type `Execute managed shell command`

![](images/oci-exec-shell-stage.png)

- Provide a name for the stage and associate it with the artifact for `oke delete`.

![](images/oci-oke-delete-stage-1.png)

- Keep the default configuration for the `Container instance` specification.

- Select a network configuration from which it can reach the OKE Cluster endpoint. We are using the node subnet of OKE for this sample.

- Click `Add` and add the stage.

![](images/oci-oke-ss-delete.png)

- During the execution it will create a new namespace of name `ns-demo-DMMYYYY` on to OKE.

- Add the below parameters to the `deployment pipeline`

```java
- OKE_ENDPOINT_TYPE: OKE Endpoint type 
- REGION : OCI Region
- OKE_OCID: OCID of OKE Cluster
```

![](images/oci-deploy-params.png)

- Click `Run pipeline` and execute the deployment pipeline.

![](images/oci-deploy-manual-run.png)

- Wait for the first stage - `OKE Deployment` to complete.

![](images/oci-deploy-stage-1-done.png)

![](images/oci-deploy-ns-created.png)


- Connect to the `OKE`, using OCI Cloud shell. You can use the `Access cluster` option to set up your OKE kubeconfig.

![](images/oci-oke-access.png)

- Run `kubectl get all -n <namespace>` and verify the deployment.

![](images/oci-kubectl-exec.png)

- Switch back to the `Deployment pipeline` and provide the approval.

![](images/oci-devops-approval.png)

- Confirm the approval and wait for the `deletion stage` to complete.

![](images/oci-kube-delete-all-stages.png)

- Validate the namespace is deleted using cloud shell - kubectl.

![](images/oci-kubectl-delete-ns.png)


### A sample command spec Yaml reference.

```java
version: 0.1
component: command
timeoutInSeconds: 10000
shell: bash
failImmediatelyOnError: true
env:
  variables:
    key: "value"
    key: "value"
  vaultVariables:
    key: "secret-id"
inputArtifacts:
  - name: artifact-name
    type: GENERIC_ARTIFACT
    artifactId: "artifact-ocid"
    registryId: OCID of the Artifact
Registry
    path: the path of the artifact in the
Registry
    version: version of the artifact
    location: target-location
  - name: artifact-name
    type: URL
    url: downloadable link
    location: target-location
steps:
  - type: Command
    name: step-name
    shell: shellType
    timeoutInSeconds: 650
    failImmediatelyOnError: true
    command: command
    onFailure:
      - type: Command
        command: |
          command
          command
        timeoutInSeconds: 400
  - type: Command
    name: step-name
    command: |
      command
      command
      command
    onFailure:
      - type: Command
        command: |
          command
        timeoutInSeconds: 400
```

- The `Shell stages` uses container instances with in the tenancies.

![](images/oci-container-instances.png)

### Cleanup the resources .

- Delete OCI Devops project with `cascade delete` option which will clean up all the devops child resources.
- Delete all the artifacts followed by the repo of OCI Artifact registry.
- Clean up the OCI Identity groups ,policies as accordingly.

Read more
----

- OCI DevOps - https://docs.oracle.com/en-us/iaas/Content/devops/using/home.htm.
- OCI Reference architectures  -  https://docs.oracle.com/solutions/
- OCI DevOps samples - https://github.com/oracle-devrel/oci-devops-examples

Contributors
===========

- Author: Rahul M R.
- Collaborators  : NA
- Last release: January 2023

### Back to examples.
----
- 🍿 [Back to OCI Devops Deployment sample](./../README.md)
- 🏝️ [Back to OCI Devops sample](./../../README.md)

