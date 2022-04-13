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
  const run = await devopsClient.getBuildRun({buildRunId: input[0].data.buildRunId});
  console.log("CURRENT BUILD RUN", JSON.stringify(run));

  var items = run.buildRun.buildOutputs.exportedVariables.items;

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
