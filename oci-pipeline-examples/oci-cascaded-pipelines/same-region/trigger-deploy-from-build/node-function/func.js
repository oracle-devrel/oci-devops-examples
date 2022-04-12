const fdk = require('@fnproject/fdk');
const common = require("oci-common");
const devops = require("oci-devops");

const deployPipelineId = "ocid1.devopsdeploypipeline.oc1.ap-hyderabad-1.amaaaaaak56z2vqavh6diwgyr4cbhqxrfmqqc6riohwyo7rvcje4vmfq5fbq";
const displayNamePrefixForNewRun = "AutoTriggeredCascade2_";

fdk.handle(async function(input){
  const provider = common.ResourcePrincipalAuthenticationDetailsProvider.builder();

  const devopsClient = new devops.DevopsClient({
    authenticationDetailsProvider: provider
  })
  const run = await devopsClient.getBuildRun({buildRunId: input[0].data.buildRunId});
  console.log("CURRENT BUILD RUN", JSON.stringify(run));

  var items = run.buildRun.buildOutputs.exportedVariables.items;

  // Add new parameters if required
  // items.push({name: 'namespace', value: 'example'});

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
