const fdk = require('@fnproject/fdk');
const common = require("oci-common");
const devops = require("oci-devops");

const deployPipelineId = "<target-deploy-pipeline-ocid>"
const displayNamePrefixForNewRun = "AutoTriggeredCascadedPipeline_";

fdk.handle(async function(input){
  const provider = common.ResourcePrincipalAuthenticationDetailsProvider.builder();

  const devopsClient = new devops.DevopsClient({
    authenticationDetailsProvider: provider
  })
  console.log("INPUT", JSON.stringify(input[0]));

  const run = await devopsClient.getDeployment({deploymentId: input[0].data.deploymentId});
  console.log("CURRENT DEPLOYMENT", JSON.stringify(run));

  var items = run.deployment.deploymentArguments.items
  
  // Add new parameters if required
  // items.push({name: 'PARAM', value: 'Value'});

  const deploymentResponse = await devopsClient.createDeployment({
    createDeploymentDetails: {
      deploymentType: "PIPELINE_DEPLOYMENT",
      deployPipelineId: deployPipelineId,
      displayName: displayNamePrefixForNewRun + new Date().toISOString(),
      deploymentArguments: {
        items
      }
    }
  })
  console.log("Deployment Response", JSON.stringify(deploymentResponse));

  return deploymentResponse;
})
