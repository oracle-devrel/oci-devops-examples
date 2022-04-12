# OCI DevOps Cascaded Pipelines

## Trigger Build Pipeline from Build Pipeline

### Prerequisites
* Two build pipelines

#### 1. Deploy Function
**Step 1:**
Clone the repository code.
```
$ git clone https://github.com/oracle-cloud-infra/oci-devops-cascaded-pipelines.git
```

**Step 2:**
Change to function directory.
```
$ cd oci-devops-cascaded-pipelines/same-region/trigger-deploy-from-build/node-function
```

**Step 3:**
In `func.js`, update `deployPipelineId` and `displayNamePrefixForNewRun` with appropriate values as below.

```
const deployPipelineId = "<target-deploy-pipeline-ocid>"
const displayNamePrefixForNewRun = "AutoTriggeredCascadedPipeline_";
```

**Step 4:**
Deploy the function with below command.
```
$ fn -v deploy --app <app-name>
```

#### 2. Configure Service Connector Hub
**Step 1:**

Open Menu > `Observability & Management` > `Service Connectors`

**Step 2:**

Set Service Connector Source as `Logging` and Target as `Functions`

**Step 3:**

Configure Source as below

![Service Connector Source Config](images/service-connector-source-config.png)

* Choose Compartment, Log Group, Logs of your DevOps Project.
* set `data.buildPipelineId` to the previous pipeline OCID as above.
* set `data.message` to the last successful unique log message like `Completed Build stage.`

**Step 4:**

Configure Target with `Function Application` and `Function` as `trigger-deploy-pipeline-from-build-pipeline` as below

![Service Connector Target Config](images/service-connector-target-config.png)

