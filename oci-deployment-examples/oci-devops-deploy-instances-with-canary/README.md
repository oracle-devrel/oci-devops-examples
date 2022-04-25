Sample illustration of OCI Devops deployment pipeline with *Canary* deployment strategies using Instance group

------------

Objective 
---

- Create OCI Devops build pipeline.
- Build a sample  application.
- Push the artifact to OCI Artifact repo.
- Use OCI Deployment pipeline with CANARY Deployment strategies.
- Validate deployment and manual role back.


Specific instructions to download only this sample.
---

```
    $ git init oci-devops-deploy-instances-with-canary
    $ cd oci-devops-deploy-instances-with-canary
    $ git remote add origin https://github.com/oracle-devrel/oci-devops-examples
    $ git config core.sparsecheckout true
    $ echo "oci-deployment-examples/oci-devops-deploy-instances-with-canary/*">>.git/info/sparse-checkout
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

- Select the type as `Instance group deployment configuration`.

![](images/devops-artifact-1.png)

- Select `Artifact source` as `Artifact Registry repository` and using `select` option ,select the Artifact repo created.

![](images/devops-artifact-2.png)

- Use a custom location ,provide a name for artifact path and version as `${BUILDRUN_HASH}`

![](images/devops-artifact-3.png)

- You can clone this repo and push to an OCI Code repo .Or create github repo by using `import` option to this repo to your GitHub profile.

    - Managing code repo for OCI Devops - https://docs.oracle.com/en-us/iaas/Content/devops/using/managing_coderepo.htm 

- Create an OCI devops build pipeline. https://docs.oracle.com/en-us/iaas/Content/devops/using/create_buildpipeline.htm 

![](images/oci-devops-buidpipeline.png)

- Add a `manage build` stage to the build pipe line . https://docs.oracle.com/en-us/iaas/Content/devops/using/add_buildstage.htm 

![](images/oci-manage-build-1.png)
![](images/oci-manage-build-1-1.png)

- Accordingly select the `code repo /connection type /repo name` for primary code repository and `save`.

If you are using a code repo other than `OCI code repo` ,ensure to set an external connection - https://docs.oracle.com/en-us/iaas/Content/devops/using/create_connection.htm 

![](images/oci-manage-build-2.png)

- Add an `Deliver artifacts` stage to the build pipeline.

![](images/oci-build-upload-artifact-1.png)

- Select the  `artifacts` created.

![](images/oci-build-upload-artifact-2.png)

- Associate the build stage `output artifact` name and `save`.

![](images/oci-build-upload-artifact-3.png)

- Snippet from [build_spec.yaml.](build_spec.yaml) with output artifacts.

```
outputArtifacts:
  - name: instace_deploy_manifest
    type: BINARY
    # this location tag doesn't effect the tag used to deliver the container image
    # to the Container Registry
    location: ${OCI_PRIMARY_SOURCE_DIR}/deploy_spec.yaml
```

- For the demo purpose we will be creating two instances of `Oracle Linux`

- Follow the document and create instances and necessary policies - https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/launchinginstance.htm 

- We will be creating `2` production instances and `1` canary instance.

- Use `Create instances`

![](images/oci-compute-create-1.png)

- Use the first instance name as `production-vm` use default placements.

![](images/oci-compute-create-2.png)

- Use Oralce Linux 8 as image and use the default shape.

![](images/oci-compute-create-3.png)

- Use a `virtual cloud network` and a public network ,Or you create one for demo using `Create new options`.

![](images/oci-compute-create-4.png)

- Use `Assign public IPV4 address` option.

- Use an appropriate `SSH Keys` option ,you would need this to login (You may use an existing one or create a new one)

- Use the `advanced` > `Oracle Cloud Agent` option and ensure that `Compute Instance Run Command` is enabled .

![](images/oci-compute-create-5-1.png)

- In the same page under `Management` add an Inline cloud-init script and a  `free-form tag` as below 

```
environment production 
```

- Add  Cloud init script is as below too ,

```
#cloud-config
users:
  - default
  - name: ocarun
    sudo: ALL=(ALL) NOPASSWD:ALL
```

![](images/oci-cloud-init-prd.png)

- Proceed the same step with a different instance name as `production-vm-1` as our second production host.

- Once done Use `Create instances` again and create a new instance for `canary`.

![](images/oci-compute-create-1.png)

- Use the  instance name as `canary-vm-1` and use default placements.

- Use Oracle Linux 8 as image and use the default shape.

![](images/oci-instance-canary-1.png)

- Use a `virtual cloud network` and a public network ,Or you create one for demo using `Create new options`.

- Use `Assign public IPV4 address` option.

![](images/oci-compute-create-4.png)

- Use an appropriate `SSH Keys` option ,you would need this to login (You may use an existing one or create a new one)

- Use the `advanced` > `Oracle Cloud Agent` option and ensure that `Compute Instance Run Command` is enabled .

![](images/oci-compute-create-5-1.png)

- In the same page under `Management` add an Inline cloud-init script and a  `free-form tag` as below 

```
environment canary
```

- Cloud init script is as below ,

```
#cloud-config
users:
  - default
  - name: ocarun
    sudo: ALL=(ALL) NOPASSWD:ALL
```

![](images/oci-cloud-init-canary.png)

- Create two new devops environment as type `Instance Group`.- https://docs.oracle.com/en-us/iaas/Content/devops/using/create_instancegroup_environment.htm 

![](images/oci-devops-env-1.png)

- Create an environment for `Production` environment.

![](images/oci-devops-env-2.png)

- Go to `next` tab and use `Query` option.

![](images/oci-devops-env-3-1.png)

- Click on `Edit query`

![](images/oci-devops-env-3.png)

- Use the query as below .

```
freeformTags.key = 'environment' && freeformTags.value = 'production'
```

- Once it list all the  `production servers` click on `Add instance query`

![](images/oci-devops-env-4.png)

- Click `Create environment` and save the config.

- Create an environment for `canary` environment.

![](images/oci-devops-env-5.png)

- Go to `next` tab and use `Query` option.

![](images/oci-devops-env-6.png)

- Click on `Edit query`

![](images/oci-devops-env-3.png)

- Use the query as below .

```
freeformTags.key = 'environment' && freeformTags.value = 'canary'
```

- Once it list the server `green-webserver` click on `Add instance query`

![](images/oci-devops-env-7.png)

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

- Select all the servers created .

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
- Do so ,use OCI `Virtual cloud networks(VCN)` service > Click on the VCN considered.

![](images/oci-vcn-1.png)

- Click on the  `Subnet` name from Subnets menu.

![](images/oci-vcn-2.png)

- Select the security list - Click  the Default one .Click on `Add ingress Rules`

![](images/oci-vcn-3.png)

- Use `Source CIDR` as 0.0.0.0/0 and `Destination Port Range` as 80 and add the rule.

![](images/oci-vcn-4.png)

![](images/oci-vcn-5.png)

- Create a new devops deployment pipeline. 
  - https://docs.oracle.com/en-us/iaas/Content/devops/using/deployment_pipelines.htm 
  - Ensure to set the correct policies ,dynamic groups to run commands on instances - https://docs.oracle.com/en-us/iaas/Content/devops/using/devops_iampolicies.htm#deploy_policies 

![](images/oci-devops-deployment.png)

- Add a stage as `Canary Strategy`.

![](images/oci-deploy-1.png)

- Select the `Deployment type` as `Instance Group` and select the `environment` created.

- Associate the `Canary environment` with the canary devops environment created.

![](images/oci-deploy-2.png)

- Select the `Instance group deployment configuration` using `Add Artifact` option .

![](images/oci-deploy-3.png)

![](images/oci-deploy-4.png)

- Select the `Load balancer` created earlier from the list.

![](images/oci-deploy-5.png)

- Select the `Listener`

![](images/oci-deploy-6.png)

- Use 80 as `Backend port`.

![](images/oci-deploy-7.png)

- Use `Instance rollout by percentage` and value as 50 (half of instances) and the `Delay between batches(seconds)` as 5 and click on `Next`.

![](images/oci-deploy-8.png)

- As it’s a demo keep the `Validation controls` as `None`or you may connect with a function to validate the deployment got to `Next`.

![](images/oci-deploy-9.png)

- Set the % of traffic to be shifted to canary (a value between 0 to 25).For this demo let us keep 25 % and click on `Next`.

![](images/oci-deploy-10.png)

- Enable the `Approval controls` and add `1` as the number of approvers and click `Next`.

![](images/oci-deploy-11.png)

- For `Production canary` stage ,associate it with the production environment and provide `50` as rollout percentage and a `Delay` of 5 seconds .

![](images/oci-deploy-12.png)

- Click add to add the stages.

![](images/oci-deploy-13.png)

 - Switch back to `Build pipeline` and add a `Trigger Deployment` stage. Select the deployment pipeline and associate. Ensure to `check` the Send build pipelines Parameters option.

![](images/oci-build-trigger-deploy.png)

![](images/oci-build-trigger-deploy-1.png)

- The build pipeline should be as below .

![](images/oci-build-trigger-deploy-2.png)

- Go back to build pipeline and do click `Start manual run`.

![](images/oci-build-run-1.png)

- Wait until all the  `build stages` completed.

![](images/oci-build-run-2.png)

- Switch to the `deployment pipeline` and click on the `Deployments` and deployment which is in `progress`.

![](images/oci-deploy-run-1.png)

- Click on it and view the progress.

![](images/oci-deploy-run-2.png)

- After a while  pipeline will be pending for `Approval` stage. Click on the 3 dots and approve the stage .

![](images/oci-deploy-approve.png)

- Wait for all the `Deployment stages` to finish.

![](images/oci-deploy-allstages.png)

- Launch the application using the public ip address via browser.

![](images/oci-chrome-prod.png)

- Now to realize the `Canary effect` ,do a re-run ,do a `manual run` of `Build pipeline`.
- Wait for all the `Build stages to finish`

![](images/oci-build-stages-all-done.png)

- Follow the `Deployments` progress and wait until `Traffic Shift to Canary` is finished (just before the approval).

![](images/oci-deploy-stage-partial.png)

- Launch the application using the public Ip address via browser. Since the canary % of shift is `25` ,25 % of request now will be served via `Canary` environment. Along the previous output you will additionally see the canary deployed application view as well. (For a demo we are using an icon to differentiate).

![](images/oci-chrome-canary.png)

- Give the `Approval` and finish the deployment .

- You may do an application change via updating the file [app_version.config](app_version.config) to a different value and re - run the `build pipeline` .

```
app_version=0.0.1 
```

- Since we are not using a test load balancer , you may launch the canary vm IP via browser to test the changes during the `Traffic shift to Canary` stage completion and approve further for production deployment and once the end of `Production Canary` stage ,the new version will be available via production load balancer.

- To do a rollback ,click on the 3 dots of Last stage of `Deployment pipeline` and use `Manual rollback`.

![](images/oci-deploy-rollback.png)

- Validate the current deployment values and references.

![](images/oci-deploy-rolleback-1.png)

- Select a valid deployment from the list and initiate the rollback.

![](images/oci-deploy-rolleback-2.png)

- Follow the progress and once done ,validate the application via production load balancer.

![](images/oci-deploy-rolleback-3.png)

- You may encounter deployment failure in case the policies ,sudo enablement or compute agent status not running on instances etc ,refer the OCI official documentations given above for such cases . Since this is made for demo we have used limited number of instances and blank sudo privilege ,which is not advised for production use cases.

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

