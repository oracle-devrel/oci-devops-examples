# OCI DevOps Cascaded Pipelines

## Objective
* Invocation of new another build or deploy pipeline after the successful execution of build/deploy pipeline.

## Prerequisites & References
This guide assumes that you already have required pipelines created to invoke them cascadly. You may refer to below links to create and setup pipelines.
* Reference Architecture - https://github.com/oracle-quickstart/oci-arch-ci-cd-devops
* Oracle DevOps Documentation - https://docs.oracle.com/en-us/iaas/Content/devops/using/home.htm
* IAM Policies - https://docs.oracle.com/en-us/iaas/Content/devops/using/devops_iampolicies.htm

## Samples

Sample procedure and code snippets for the cascaded pipelines of the below scenarios.

* [Trigger Build Pipeline from Build Pipeline](same-region/trigger-build-from-build)
* [Trigger Deploy Pipeline from Build Pipeline](same-region/trigger-deploy-from-build)
* [Trigger Build Pipeline from Deploy Pipeline](same-region/trigger-build-from-deploy)
* [Trigger Deploy Pipeline from Deploy Pipeline](same-region/trigger-deploy-from-deploy)


