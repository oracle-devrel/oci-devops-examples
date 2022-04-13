const fdk = require('@fnproject/fdk');
const common = require("oci-common");
const devops = require("oci-devops");

const buildPipelineId = process.env.build_pipeline_id;
const displayNamePrefixForNewRun = process.env.display_name_prefix_for_new_run;

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

  const buildRunResponse = await devopsClient.createBuildRun({
    createBuildRunDetails: {
      buildPipelineId,
      displayName: displayNamePrefixForNewRun + new Date().toISOString(),
      buildRunArguments: {
        items
      }
    }
  })
  console.log("CREATE BUILD RUN RESPONSE", JSON.stringify(buildRunResponse));

  return buildRunResponse;
})
