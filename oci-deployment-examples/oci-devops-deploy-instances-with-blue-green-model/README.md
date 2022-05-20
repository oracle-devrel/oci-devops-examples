Sample illustration of OCI Devops deployment pipeline with *BLUE-GREEN* deployment strategies using Instance group

------------

Objective 
---

- Create OCI Devops build pipeline.
- Build a sample  application.
- Push the artifact to OCI Container and OCI Artifact repo.
- Use OCI Deployment pipeline with BLUE/GREEN Deployment strategies.
- Validate deployment and manual role back.

Specific instructions to download only this sample.
---

```
    $ git init oci-devops-deploy-instances-with-blue-green-model
    $ cd oci-devops-deploy-instances-with-blue-green-model
    $ git remote add origin https://github.com/oracle-devrel/oci-devops-examples
    $ git config core.sparsecheckout true
    $ echo "oci-deployment-examples/oci-devops-deploy-instances-with-blue-green-model/*">>.git/info/sparse-checkout
    $ git pull --depth=1 origin main

```

Procedure
---

- Create an OCI artifact registry & associated policies. https://docs.oracle.com/en-us/iaas/Content/artifacts/home.htm 

![](images/oci-artifact-repo.png)

- Set policies & create a devops project - https://docs.oracle.com/en-us/iaas/Content/devops/using/home.htm.
- Devops policies - https://docs.oracle.com/en-us/iaas/Content/devops/using/getting_started.htm#prereq. 

![](images/oci-devops-project.png)

- Create devops artifacts. - https://docs.oracle.com/en-us/iaas/Content/devops/using/artifacts.htm 

- Select the types as `Instance group deployment configuration`.

![](images/devops-artifact-1.png)

- Select `Artifact source` as `Artifact Registry repository` and using `select` option ,select the Artifact repo created.

![](images/devops-artifact-2.png)

- Use a custom location ,provide a name for artifact path and version as `${BUILDRUN_HASH}`

![](images/devops-artifact-3.png)

- You can clone this repo and push to an OCI Code repo .Or create GitHub repo by using `import` option to this repo to your GitHub profile.

    - Managing code repo for OCI Devops - https://docs.oracle.com/en-us/iaas/Content/devops/using/managing_coderepo.htm 

- Create an OCI devops build pipeline. https://docs.oracle.com/en-us/iaas/Content/devops/using/create_buildpipeline.htm 

![](images/oci-devops-buidpipeline.png)

- Add a `manage build` stage to the build pipe line . https://docs.oracle.com/en-us/iaas/Content/devops/using/add_buildstage.htm 

![](images/oci-manage-build-1.png)
![](images/oci-manage-build-1-1.png)

- Accordingly select the `code repo /connection type /repo name` for primary code repository and `save`.

If you are using a code repo other than `OCI code repo` ,ensure to set an external connection - https://docs.oracle.com/en-us/iaas/Content/devops/using/create_connection.htm 

![](images/oci-manage-build-2.png)

- Add an `Deliver artifact` stage to the build pipeline.

![](images/oci-build-upload-artifact-1.png)

- Select the  `artifacts` created.

![](images/oci-build-upload-artifact-2.png)

- Associate the build stage `output artifact` name and `save`.

![](images/oci-build-upload-artifact-3.png)

- Snippet from [build_spec.yaml.](build_spec.yaml) with output artifacts.

```
outputArtifacts:
  - name: instance_deploy_manifest
    type: BINARY
    # this location tag doesn't effect the tag used to deliver the container image
    # to the Container Registry
    location: ${OCI_PRIMARY_SOURCE_DIR}/deploy_spec.yaml
```

- For the demo purpose we will be creating two instances of `Oracle Linux`

- Follow the document and create instances and necessary policies - https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/launchinginstance.htm 

- Use `Create instances`

![](images/oci-compute-create-1.png)

- Use the first instance name as `blue-webserver` use default placements.

![](images/oci-compute-create-2.png)

- Use Oracle Linux 8 as image and use the default shape.

![](images/oci-compute-create-3.png)

- Use a `virtual cloud network` and a public network ,Or you create one for demo using `Create new options`.

![](images/oci-compute-create-4.png)

- Use `Assign public IPV4 address` option.

- Use an appropriate `SSH Keys` option ,you would need this to login (You may use an existing one or create a new one)

- Use the `advanced` > `Oracle Cloud Agent` option and ensure that `Compute Instance Run Command` is enabled .

![](images/oci-compute-create-5.png)

- In the same page under `Management` add an Inline cloud-init script and a  `free-form tag` as below 

```
environment blue
```

- Cloud init script is as below ,

```
#cloud-config
users:
  - default
  - name: ocarun
    sudo: ALL=(ALL) NOPASSWD:ALL
```

![](images/oci-cloud-init-blue.png)

- Use `Create instances` and create a new instances.

![](images/oci-compute-create-1.png)

- Use the first instance name as `green-webserver` use default placements.

- Use Oracle Linux 8 as image and use the default shape.

![](images/oci-instance-green-1.png)

- Use a `virtual cloud network` and a public network ,Or you create one for demo using `Create new options`.

- Use `Assign public IPV4 address` option.

![](images/oci-compute-create-4.png)

- Use an appropriate `SSH Keys` option ,you would need this to login (You may use an existing one or create a new one)

- Use the `advanced` > `Oracle Cloud Agent` option and ensure that `Compute Instance Run Command` is enabled .

![](images/oci-compute-create-5.png)

- In the same page under `Management` add an Inline cloud-init script and a  `free-form tag` as below 

```
environment green
```

- Cloud init script is as below ,

```
#cloud-config
users:
  - default
  - name: ocarun
    sudo: ALL=(ALL) NOPASSWD:ALL
```

![](images/oci-cloud-init-green.png)

- Create two new devops environment as type `Instance Group`.- https://docs.oracle.com/en-us/iaas/Content/devops/using/create_instancegroup_environment.htm 

![](images/oci-devops-env-blue-1.png)

- Create an environment for `Blue` environment.

![](images/oci-devops-env-blue-2.png)

- Go to `next` tab and use `Query` option.

![](images/oci-devops-env-blue-3.png)

- Click on `Edit query`

![](images/oci-devops-env-blue-4.png)

- Use the query as below .

```
freeformTags.key = 'environment' && freeformTags.value = 'blue'
```

- Once it list the server `blue-webserver` click on `Add instance query`

![](images/oci-devops-env-blue-5.png)

- Click `Create environment` and save the config.

- Create an environment for `green` environment.

![](images/oci-devops-env-green-1.png)

- Go to `next` tab and use `Query` option.

![](images/oci-devops-env-blue-3.png)

- Click on `Edit query`

![](images/oci-devops-env-blue-4.png)

- Use the query as below .

```
freeformTags.key = 'environment' && freeformTags.value = 'green'
```

- Once it list the server `green-webserver` click on `Add instance query`

![](images/oci-devops-env-green-2.png)

- Click `Create environment` and save the config.

- Now let us create a new `Load Balancers` under `Networking`

![](images/oci-lb-1.png)

- Use `Load Balancer` wizard.

![](images/oci-lb-2.png)

- Provide a name and use `Public` visibility and IP address as `Ephemeral IP`.

![](images/oci-lb-3.png)

- Use default shapes and select the  Virtual Cloud Network and Subnet same as that of the the instances created.

![](images/oci-lb-4.png)

- Use `Next` and click on `Add Backends`

![](images/oci-lb-5.png)

- Select the server created .

![](images/oci-lb-6.png)

- As this a test ,select the Health check policy as `http` and port as `80` and go next.

![](images/oci-lb-7.png)

- Configure a `http` listener.

![](images/oci-lb-8.png)

- Keep the logs with `default` options and `Submit`

![](images/oci-lb-9.png)

- Wait until the load balancer become active.

![](images/oci-lb-10.png)

- We need to create an ingress rule to allow our application traffic .
- Do so ,use OCI `Virtual cloud networks(VCN)` service > Click on the VCN used.

![](images/oci-vcn-1.png)

- Click on the  `Subnet` name from Subnets menu.

![](images/oci-vcn-2.png)

- Select the security list - use the Default one .Click on `Add ingress Rules`

![](images/oci-vcn-3.png)

- Use `Source CIDR` as 0.0.0.0/0 and `Destination Port Range` as 80 and add the rule.

![](images/oci-vcn-4.png)

![](images/oci-vcn-5.png)

- Create a new devops deployment pipeline. 
  - https://docs.oracle.com/en-us/iaas/Content/devops/using/deployment_pipelines.htm 
  - Ensure to set the correct policies ,dynamic groups to run commands on instances - https://docs.oracle.com/en-us/iaas/Content/devops/using/devops_iampolicies.htm#deploy_policies 

![](images/oci-devops-deployment.png)

- Add a stage as `Blue/Green Strategy`.

![](images/oci-deploy-stage-bg-1.png)

- Select the `Deployment type` as `Instance Group` and select the `environment` created.

- Associate the `instance environments` created.

![](images/oci-deploy-stage-bg-2.png)

- Select the `Instance group deployment configuration` using `Add Artifact` option .

![](images/oci-deploy-stage-bg-3.png)

![](images/oci-deploy-stage-bg-4.png)

- Select the `Load balancer` created earlier from the list.

![](images/oci-deploy-stage-bg-5.png)

- Select the `Listener`

![](images/oci-deploy-stage-bg-6.png)

- Use 80 as `Backend port`.

![](images/oci-deploy-stage-bg-7.png)

- Update instance rollout policy by percentage and keep the value as  `100` and Click `Next`.

![](images/oci-deploy-stage-bg-8.png)

- As its a demo keep the `Validation controls` as `None ‘or you may connect with a function to validate the deployment.

![](images/oci-deploy-bg-validation.png)

- Enable the `Approval controls` and add `1` as the number of approvers.

![](images/oci-deploy-approval.png)

- Click add to add the stages.

![](images/oci-deploy-all-stages.png)

 - Switch back to `Build pipeline` and add a `Trigger Deployment` stage. Select the deployment pipeline and associate. Ensure to `check` the Send build pipelines Parameters option.

![](images/oci-build-trigger-deploy.png)

![](images/oci-build-trigger-deploy-1.png) 

- The build pipeline should be as below .

![](images/oci-build-trigger-deploy-2.png)

Let's Test
-------

- Go back to build pipeline and do click `Start manual run`.

![](images/oci-build-run-1.png)

- Wait until all the  `build stages` completed.

![](images/oci-build-run-2.png)

- Switch to the `deployment pipeline` and click on the `Deployments` and deployment which is in `progress`.

![](images/oci-deploy-bg-1.png)

- After a while  pipeline will be pending for `Approval` stage. Click on the 3 dots and approve the stage .

![](images/oci-deploy-approve.png)

- Switch back to `Network>Load balancer` and fetch the public IP address .

![](images/oci-lb-ip-address.png)

- Switch back to `Deployment pipeline` and validate the completion of all steps.

![](images/oci-deploy-allstages.png)

- Launch the application via a browser and validate the deployment.

![](images/oci-lb-view-1.png)

The expected result would be 

```
With Love from OCI Devops(Version:<Value>) ,Served via environment:<GREEN or BLUE>

```

- Let us do a new deployment ,by changing app version in the file [app_version.config.](app_version.config)

```
app_version=2.0.0
```

- Push back to the respective code repo ,followed by a manual run of `Build pipeline` and wait for the completion of build and deployment pipeline (with an approval phase as well ).


- If you wish to validate the service before going to production (That’s the best practice for production deployment ,you can add a test load-balancer to fetch the intermittent version release.).For a demo you may validate by launching the instance's public IP via the browser.

- Refresh the browser with load-balancer IP and validate the changes .

![](images/oci-lb-view-2.png)

- You validate  the environment switch as accordingly.

- You may encounter issues mostly  if the ,oci compute agent , sudo or policies are not set correct ,so please re validate the polices and dynamic groups as per the documents accordingly.

- You may also encounter  `502 bad gateway` during a traffic shift ,as this a demo we are not really persisting the state or maintaining any graceful switch over , these momentarily  errors are normal.

- To do a role back , use the `Revert traffic shift` option via the last stage.

![](images/oci-deploy-revert.png)

- Validate the current deployment values.

![](images/oci-deploy-revert-1.png)

- Also validate the new deployment (rollback version) values.

![](images/oci-deploy-revert-2.png)

- You can click `Reverse Traffic Shift` button to launch the rollback.

![](images/oci-deploy-revert-3.png)

- Wait for the completion and validate the result via load-balancer IP address over a browser.

![](images/oci-deploy-revert-4.png)

![](images/oci-deploy-revert-5.png)

Read more 
----

- OCI Devops - https://docs.oracle.com/en-us/iaas/Content/devops/using/home.htm.
- OCI Reference architectures  -  https://docs.oracle.com/solutions/
- OCI Devops samples - https://github.com/oracle-devrel/oci-devops-examples 

Contributors 
===========

- Author : Rahul M R.
- Collaborators  : NA
- Last release : March 2022

### Back to examples.
----

- 🍿 [Back to OCI Devops Deployment sample](./../README.md)
- 🏝️ [Back to OCI Devops sample](./../../README.md)
