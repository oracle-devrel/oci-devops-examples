# Sample illustration of invoking a OCI Devops Deployment pipeline with [OCI Github actions](https://blogs.oracle.com/cloud-infrastructure/post/github-actions-with-oci).

## Objective

- Define new GitHub Actions with OCI to upload a container image and invoke a deploy.
- Execute a GitHub Action workflow and validate the deployment.

```bash
git init oci-devops-githubactions-deploy
cd oci-devops-githubactions-deploy
git remote add origin https://github.com/oracle-devrel/oci-devops-examples
git config core.sparsecheckout true
echo "oci-deployment-examples/oci-devops-githubactions-deploy/*">>.git/info/sparse-checkout
git pull --depth=1 origin main
```

## Prerequisites

- access to a OCI Tenancy (free tier or paid)
- a GitHub account

## Procedure

- Create or fetch below values and make a note as you will be storing them as GitHub secrets.
- Refer here for more: <https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcredentials.htm>

```yaml
OCI_AUTH_TOKEN:
  token_string # generated via the OCI Console or CLI tool
OCI_CLI_FINGERPRINT: |
  a1:bb:c1:dd:e1:ff:a2:b2:c2:d2:e2:f2:3a:3b:3c:3d
OCI_CLI_KEY_CONTENT: |
  -----BEGIN PRIVATE KEY-----
  MIIE.......................................................cMo+z
  ...
  ...
  MqN4EaoFLH6jQ1bYVI+HZkh9
  -----END PRIVATE KEY-----
OCI_CLI_REGION: |
  us-ashburn-1
OCI_CLI_TENANCY: |
  ocid1.tenancy.oc1.....
OCI_CLI_USER: |
  ocid1.user.oc1.....
OCI_COMPARTMENT_OCID: |
  ocid1.compartment.oc1.....
```

- Create a dynamic group and add below rules.

```javascript
ALL {resource.type = 'devopsdeploypipeline', resource.compartment.id = 'OCID of the Compartment'}
```

- Create a policy on to the dynamic group.

```javascript
Allow dynamic-group <NAME of the DYNAMIC GROUP> to manage  cluster-family in compartment <COMPARTMENT NAME>
Allow dynamic-group <NAME of the DYNAMIC GROUP> to manage  ons-topics in compartment <COMPARTMENT NAME>
Allow dynamic-group <NAME of the DYNAMIC GROUP> to manage  repos in compartment <COMPARTMENT NAME>
```

- Create an OCI notification topic. - <https://docs.oracle.com/en-us/iaas/Content/Notification/Tasks/managingtopicsandsubscriptions.htm#createTopic>
- Create an Oracle Container Engine for Kubernetes (OKE) cluster - <https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengcreatingclusterusingoke_topic-Using_the_Console_to_create_a_Quick_Cluster_with_Default_Settings.htm#create-quick-cluster>

- Create an OCI devops project - <https://docs.oracle.com/en-us/iaas/Content/devops/using/create_project.htm#create_a_project>

![](images/oci-devops-project.png)

- Ensure to enable the `logs` for the devops project.

![](images/oci-devops-logs.png)

- Create a new devops environment of type `Kubernetes Cluster` and associate with the OKE cluster created- <https://docs.oracle.com/en-us/iaas/Content/devops/using/create_oke_environment.htm>

![](images/oci-devops-env.png)

- Create a devops artifact of type `Kubernetes manifest` - <https://docs.oracle.com/en-us/iaas/Content/devops/using/artifacts.htm>

![](images/oci-devops-artifact-1.png)

- Select `Inline` as Artifact source.

![](images/oci-devops-artifact-2.png)

- Copy the content of file [deploymentmanifest.yaml](deploymentmanifest.yaml) as value.

![](images/oci-devops-artifact-value.png)

- Replace the placeholders in the `image` field with the correct values for the `region` and `namespace`. For example:

```yaml
image: us-sanjose-1.ocir.io/my_name_space/python_fastapi_app:${image_tag}
```

- Ensure that the option `Allow parameterization` is checked in.

![](images/oci-devops-artifact-3.png)

- Create a new deployment pipeline - <https://docs.oracle.com/en-us/iaas/Content/devops/using/deployment_pipelines.htm>

![](images/oci-devops-deploymentpipeline.png)

- Use `+` and add  new stage as `Deploy OKE`

![](images/oci-deployment-oke-stage.png)

- Provide a stage name.

![](images/oci-deploy-stage-name.png)

- Associate with the `devops artifact` and `devops environment` created with the stage.Create stage.

![](images/oci-deploy-stage-env-artifact.png)

![](images/oci-deploypipeline-final.png)

- Click on the `Parameters` and add below key and values.

| Name | Example values |
| ---- | ------- |
| `image_tag` | `0` |
| `namespace` | `ns-github` |


We will override these values from GitHub Actions while executing.

![](images/oci-deploy-params.png)

- Switch back to Devops project overview, click on `Deployment Pipelines`, click `copy` under OCID and make a note of  the OCID of the deployment pipeline.

![](images/oci-deploy-ocid.png)

- Login to `https://github.com`.

- Click on `Profile icon` > `Settings`

![](images/oci-github-settings.png)

- Click on `Developer settings`

![](images/oci-git-devsettings.png)

- Create a new `Personal access token`

![](images/oci-github-pat.png)

- Ensure to select `Repo` and `Workflow` access as minimum. Use the expiration duration as accordingly.

![](images/oci-github-permissions.png)

Make a note of the `PAT`

- Click `+` and create a new repository.

![](images/oci-github-create-new.png)

![](images/oci-github-new-repo.png)

- Click `Settings`

![](images/oci-repo-settings.png)

- Select `Secrets` > `Action`.

![](images/oci-gitrepo-secrets.png)

- Click `New repoistory secrets` and add below values.You do not need to use them with ""

```yaml
DEPLOYMENT_PIPELINE_OCID: OCID of deployment pipeline
OCI_AUTH_TOKEN: User access token.
OCI_CLI_FINGERPRINT:  User fingerprint.
OCI_CLI_KEY_CONTENT: User ssh public key.
OCI_CLI_REGION: OCI Region.
OCI_CLI_TENANCY: OCID of tenancy
OCI_CLI_USER: OCID of the user.
OCI_COMPARTMENT_OCID: OCID of the compartment
```

![](images/oci-github-secrets-list.png)

- The file [oci_actions.yaml](.github/workflows/oci_actions.yml) contains an example GitHub Actions workflow.

```yaml
name: OCI Deploy
# Controls when the workflow will run
on:
  # this workflow will be triggered whenever something is pushed to the main branch.
  push:
    branches: [ "main"]
  # You can add more branches or more events.

jobs:
  invoke-oci-deployment:
    runs-on: ubuntu-latest
    name: Invoke OCI Deployment from GitHub to OKE
    env:  # These are the credentials used by OCI GitHub Actions
      OCI_CLI_USER: ${{ secrets.OCI_CLI_USER }}
      OCI_CLI_TENANCY: ${{ secrets.OCI_CLI_TENANCY }}
      OCI_CLI_FINGERPRINT: ${{ secrets.OCI_CLI_FINGERPRINT }}
      OCI_CLI_KEY_CONTENT: ${{ secrets.OCI_CLI_KEY_CONTENT }}
      OCI_CLI_REGION: ${{ secrets.OCI_CLI_REGION }}

    steps:
      - name: Check out code
        uses: actions/checkout@v2


      # This step will return the URL for the a container registry repo or create a new one
      - name: Get or create an OCIR Repository
        uses: oracle-actions/get-ocir-repository@v1.0
        id: get-ocir-repository
        with:
          name: python_fastapi_app
          compartment: ${{ secrets.OCI_COMPARTMENT_OCID }}

      # This step provides credentials to both Docker and Podman to the OCIR repo (even if its private) using access token
      - name: Log into OCIR
        uses: oracle-actions/login-ocir@v1.0
        id: login-ocir
        with:
          auth_token: ${{ secrets.OCI_AUTH_TOKEN }}

      # This step builds the container image and pushes it to the OCIR repo found in step 2 using the credentials from step 3
      - name: Tag and push a container image <== Create a container image.
        id: tag-and-push-image
        run: |
          docker build -t "${{ steps.get-ocir-repository.outputs.repo_path }}:$GITHUB_RUN_NUMBER" .
          docker push "${{ steps.get-ocir-repository.outputs.repo_path }}:$GITHUB_RUN_NUMBER"

      # This step generates the deployment arguments in JSON format
      - name: Generate deployment arguments
        id: create-json
        run: |
          echo "::set-output name=deployargs::{\"items\":[{\"name\":\"namespace\",\"value\":\"ns-github\"},{\"name\":\"image_tag\",\"value\":\"$GITHUB_RUN_NUMBER\"}]}"

      # This step invokes the deployment pipeline using the JSON from the previous step
      - name: Invoke deployment pipeline <== Invoke the deployment
        uses: oracle-actions/run-oci-cli-command@v1.0
        id:  invoke-deployment
        with:
          command: devops deployment create-pipeline-deployment --pipeline-id ${{ secrets.DEPLOYMENT_PIPELINE_OCID }} --deployment-arguments ${{ toJSON(steps.create-json.outputs.deployargs) }}
```

![](images/oci-containerregistry-repo.png)

## Create a push and invoke the GitHub Action workflow

- Add the content and push to the repository.

```bash
git remote add origin <Github repo url>
git branch -M main
git push -u origin main
```

- Click on `Actions under the repo`

![](images/oci-github-actions.png)

- View the workflow and you should see each action as it runs.

![](images/oci-github-run.png)

- Click details and view the actions.

![](images/oci-github-actions-details.png)

- Wait for the all the steps to complete.

![](images/oci-github-action-steps.png)

- Click on the steps and you can get more details

![](images/oci-github-action-deploy-steps.png)

- You may encounter issues mostly if the secrets are wrong or missed the polices or dynamic groups.
- You should see a new container image is pushed to the container registry repo and a new deployments is in progress under the deployment pipeline.

![](images/oci-container-registry-repo.png)

![](images/oci-deployment-view.png)

- Connect to `OKE Cluster`, using OKE - `Access Cluster` steps.

![](images/oci-oke-cluster-access.png)

- Once connected to OKE via cloud shell or local access. Run below and fetch the public IP and validate the application.

```bash
kubectl get all -n ns-github
```

- Access the application via curl `curl http://<EXTERNAL IP >` or via browser.

![](images/oci-app-view.png)

## Read more

- OCI Devops - <https://docs.oracle.com/en-us/iaas/Content/devops/using/home.htm>
- OCI Reference architectures  -  <https://docs.oracle.com/solutions/>
- OCI Devops samples - <https://github.com/oracle-devrel/oci-devops-examples>

## Contributors

- Author : [Rahul M R](https://github.com/RahulMR42).
- Collaborators : NA
- Last release : July 2022

### Back to examples

- 🍿 [Back to OCI Devops Deployment sample](./../README.md)
- 🏝️ [Back to OCI Devops sample](./../../README.md)
