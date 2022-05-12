

Sample illustration of OCI Devops deployment pipeline with *BLUE-GREEN* deployment strategies using Oracle Container Engine for Kubernetes (OKE).

------------

Objective 
---

- Create OCI Devops build pipeline.
- Build a sample python application.
- Push the artifact to OCI Container and OCI Artifact repo.
- Use OCI Deployment pipeline with BLUE/GREEN Deployment strategies.
- Validate deployment and manual role back.

Specific instructions to download only this sample.
---

```
    $ git init oci-devops-deploy-with-blue-green-model
    $ cd oci-devops-deploy-with-blue-green-model
    $ git remote add origin https://github.com/oracle-devrel/oci-devops-examples
    $ git config core.sparsecheckout true
    $ echo "oci-deployment-examples/oci-devops-deploy-with-blue-green-model/*">>.git/info/sparse-checkout
    $ git pull --depth=1 origin main

```


Procedure
---

- Create an OCI container registry . https://docs.oracle.com/en-us/iaas/Content/Registry/home.htm 

![](images/oci-container-repo.png)

- Create an OCI artifact registry . https://docs.oracle.com/en-us/iaas/Content/artifacts/home.htm 

![](images/oci-artifact-repo.png)

- Set policies & create a devops project - https://docs.oracle.com/en-us/iaas/Content/devops/using/home.htm.

![](images/oci-devops-project.png)

- Create devops artifacts. - https://docs.oracle.com/en-us/iaas/Content/devops/using/artifacts.htm 

- Create an artifact with type `Docker image` for build to push the artifact. Ensure use your `container repo` URL, with `${BUILDRUN_HASH}` at the end of the URL. This is to make the docker image version as dynamic.

![](images/oci-devops-artifact-docker.png)

   
- Create an artifact as type `Kubernetes manifest`.Ensure to add your `artifact repo` path and version as `${BUILDRUN_HASH}` .

![](images/oci-artifact-repo-path.png)

![](images/oci-artifact-repo-path-2.png)


- You can clone this repo and push to an OCI Code repo .Or create GitHub repo by using `import` option to this repo to your GitHub profile.

    - Managing code repo for OCI Devops - https://docs.oracle.com/en-us/iaas/Content/devops/using/managing_coderepo.htm 

- Create an OCI devops build pipeline. https://docs.oracle.com/en-us/iaas/Content/devops/using/create_buildpipeline.htm 

![](images/oci-devops-buidpipeline.png)

- Add a `manage build` stage to the build pipe line . https://docs.oracle.com/en-us/iaas/Content/devops/using/add_buildstage.htm 

![](images/oci-manage-build-1.png)
![](images/oci-manage-build-1-1.png)

- Accordingly select the `code repo /connection type /repo name`.

If you are using a code repo other than `OCI code repo` ,ensure to set an external connection - https://docs.oracle.com/en-us/iaas/Content/devops/using/create_connection.htm 

![](images/oci-manage-build-2.png)

- Add an `Deliver artifact` stage to the build pipeline.

![](images/oci-build-upload-artifact-1.png)

- Select the two `artifacts` created.

![](images/oci-build-upload-artifact-2.png)

- Associate the build stage `output artifact` names .

![](images/oci-build-upload-artifact-3.png)

- Snippet from [build_spec.yaml.](build_spec.yaml) with output artifacts.

```
outputArtifacts:
  - name: oke_app_base
    type: DOCKER_IMAGE
    # this location tag doesn't effect the tag used to deliver the container image
    # to the Container Registry
    location: oke_app_base:latest

  - name: oke_deploy_manifest
    type: BINARY
    # this location tag doesn't effect the tag used to deliver the container image
    # to the Container Registry
    location: ${OCI_PRIMARY_SOURCE_DIR}/oci-oke-deployment.yaml
```

- Create a new OKE (With public endpoint and public or private workers) - https://docs.oracle.com/en-us/iaas/Content/ContEng/home.htm .You may reuse an existing one accordingly . Use `Access cluster` option to set your access to `OKE`.

![](images/oci-oke.png)

- Create a new devops environment as type `Kubernetes Cluster`.-https://docs.oracle.com/en-us/iaas/Content/devops/using/create_oke_environment.htm  

![](images/oci-devops-oke-env.png)
![](images/oci-devops-oke-env-2.png)

- Create a new devops deployment pipeline. - https://docs.oracle.com/en-us/iaas/Content/devops/using/deployment_pipelines.htm 

![](images/oci-devops-deployment.png)

- Add a stage as `Blue/Green Strategy`.

![](images/oci-deploy-stage-bg-1.png)

- Select the `Deployment type` as `OKE` and select the `environment` created.

- Associate the `oke environment` created.

![](images/oci-deploy-stage-bg-2.png)

- Select Namespace A as `ns-green` and Namespace B as `ns-blue`.(These are names for test ,you may use other names accordingly)

![](images/oci-deploy-stage-bg-3.png)

- Select the `Kubernetes Artifacts`.

![](images/oci-deploy-stage-bg-4.png)

- Fill the ingress name as `sample-oke-bg-app-ing` .It’s the sample ingress name declared via [deployment manifest.](oci-oke-deployment.yaml)

![](images/oci-deploy-stage-bg-5.png)

- As its a demo keep the `Validation controls` as `None` or you may connect with a function to validate the deployment.

![](images/oci-deploy-bg-validation.png)

- Enable the `Approval controls` and add `1` as the number of approvers.

![](images/oci-deploy-approval.png)

- Click add to add the stages.

![](images/oci-deploy-all-stages.png)

 - Switch back to `Build pipeline` and add a `Trigger Deployment` stage. Select the deployment pipeline and associate. Ensure to `check` the Send build pipelines Parameters option.

 ![](images/oci-build-trigger-deploy.png)

- In order to run the blue green we should install `Nginx Ingress Controller` to our `OKE` cluster.
- Launch `OCI Cloud shell` to enable the OKE access.
- Follow the instruction via `Access Cluster` tab for the OKE cluster.

![](images/oci-oke.png)

- Validate the Kubernetes access using `kubectl get nodes` & `kubectl config view`.

![](images/kubectl-get-nodes.png)

- We will be following the procedure to install and setup `Ingress Controller` - https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengsettingupingresscontroller.htm 

- Create a `clusterrolebinding` with user `ocid`.

```
kubectl create clusterrolebinding oke_cluster_role_<username> --clusterrole=cluster-admin --user=ocid1.user.oc1..xxx
```

- Install the Ingress controller, always use the latest version. - https://github.com/kubernetes/ingress-nginx#changelog 

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.2/deploy/static/provider/cloud/deploy.yaml
```

- Create and save the file cloud-generic.yaml containing the following code to define the ingress-nginx ingress controller service as a load balancer service.

```
kind: Service
apiVersion: v1
metadata:
  name: ingress-nginx
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
spec:
  type: LoadBalancer
  selector:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
  ports:
    - name: http
      port: 80
      targetPort: http
    - name: https
      port: 443
      targetPort: https

```

- Using the file you just saved, create the ingress-nginx ingress controller service by running the following command.

```
kubectl apply -f cloud-generic.yaml
```

- You may follow the procedure to create a TLS certificate for nginx.

```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=nginxsvc/O=nginxsvc"
kubectl create secret tls tls-secret --key tls.key --cert tls.crt
```

- You may skip the sample application example in the procedure.

- Validate the installation.

```
kubectl get svc -n ingress-nginx
```
- The EXTERNAL-IP for the ingress-nginx ingress controller service is shown as `pending` until the load balancer has been fully created in Oracle Cloud Infrastructure. Repeat the kubectl get svc command until an EXTERNAL-IP is shown for the ingress-nginx ingress controller service.

![](images/kubectl-get-svc.png)

- Create two new namespaces for the deployment.

```
kubectl create ns ns-blue;kubectl create ns  ns-green
```

- Go back to build pipeline and do click `Start manual run`.

![](images/oci-build-run-1.png)

- Wait until all the  `build stages` completed.

![](images/oci-build-run-2.png)

- Switch to the `deployment pipeline` and click on the deployment which is in `progress`.

![](images/oci-deploy-bg-1.png)

- The pipeline will be pending for `Approval` stage.
- Validate the first deployment at this stage. You should see a valid deployments at namespace `ns-green`.

```
for i in ns-green ns-blue ; do echo "-- NS:$i --";kubectl get po,ing -n $i; done

```

![](images/oci-deploy-bg-validate-1.png)

- Click on the `3 dots` and validate the `Control:Approval` stage.

![](images/oci-deploy-bg-approval-1.png)
![](images/oci-deploy-bg-approval-2.png)

- Wait for all the steps to complete.

![](images/oci-deploy-bg-all-stages.png)

- Validate the deployment using the `Ingress Address`.

```
curl -k http://<Ingress Address>
```

- Edit the source code - `main.py` and change the version to `0.1` and run the build pipeline again to test a new deployment scenario.

```
from typing import Optional

from fastapi import FastAPI

import os

app = FastAPI()

@app.get("/")
def read_root():
    version="0.0"
    namespace = os.getenv('POD_NAMESPACE', default = 'ns-red')
    return {"Message": "with Love from OCI Devops ","Version":version,"Namespace":namespace}
```


Let's Test
-------


- Go back to build pipeline and do click `Start manual run`.

![](images/oci-build-run-1.png)

- Wait untill all the  `build stages` completed.

![](images/oci-build-run-2.png)

- Switch to the `deployment pipeline` and click on the deployment which is in `progress`.

![](images/oci-deploy-bg-1.png)

- The pipeline will be pending for `Approval` stage.
- Validate the first deployment at this stage. You should see a valid deployments at namespace `ns-blue` too.

```
for i in ns-green ns-blue ; do echo "-- NS:$i --";kubectl get po,ing -n $i; done

```

![](images/oci-deploy-bg-stage-2.png)

- Validate the deployment using the `Ingress Address`.

```
curl -k http://<Ingress Address>
```

Output :

```
{"Message":"with Love from OCI Devops ","Version":"0.1","Namespace":"ns-blue"}
```

- You can continue other re-run from build pipeline and validate the switch between environment.

- Let us now try a `Manul rollback`.

- Use the `3 dots` at the stage `Traffic Shift` stage and select `Manual Rollback`.

![](images/oci-deploy-bg-roleback-1.png)

- Select a previously successful deployment.

![](images/oci-deploy-bg-roleback-2.png)

- Close the `select deployment` page and click `Rollback Stage` option.

![](images/oci-deploy-bg-roleback-3.png)

- Wait for stage to complete .

![](images/oci-deploy-bg-rolleback-done.png)

- Validate the deployment using the `Ingress Address`.

```
curl -k http://<Ingress Address>
```

Output :

```
{"Message":"with Love from OCI Devops ","Version":"0.0","Namespace":"ns-green"}
```

Note : Re-Run of deployment pipeline with OKE Blue-Green stage is not supported for now.

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


