Sample illustrations of `dynamic groups` and `policies` requirements for `OCI Devops` and few connected OCI services.

----------

### ❗ Attention please:

- All these samples are written with a sample dynamic groups,please change accordingly. 
- All the policies are using verbs * manage or use * which are powerfull , you may alter with other verbs( read,inspect) as accordingly.
- Use the [References](https://github.com/RahulMR42/oci-devops-policies-groups#references) section to read more about fine grain controls. 


* Specific instruction to clone only this example.

    ```
    $ git init oci-devops-policies-groups
    $ cd oci-devops-policies-groups
    $ git remote add origin https://github.com/oracle-devrel/oci-devops-examples
    $ git config core.sparsecheckout true
    $ echo "oci-config-examples/oci-devops-policies-groups/*">>.git/info/sparse-checkout
    $ git pull --depth=1 origin main

    ```

<!-- All about user groups  -->

### ✔️ User Groups

<details>
<summary>Devops Pipeline (OCI Repo + Build + Deploy) - Click to expand</summary>

-  Create  relevenat users and all the devops users to the user group (One group is minimum).
-  You may use `Administrator` group for devops ,however better to create a specific user group to have better control.
- For further controls ,you may create different user groups like `devops-admins`,`devops-users`,`devops-validators` etc.
- Documentation
    - How to create user groups - https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managinggroups.htm#three
    - How to add users to user groups - https://docs.oracle.com/en-us/iaas/Content/devops/using/getting_started.htm#prereq 

</details>

<!-- All about dynamic  groups -->

### ✔️ Dynamic Groups 

<details>
<summary>Devops Pipeline (OCI Repo + Build + Deploy) - Click to expand</summary>

- Create dynamic group (EG: dg-compartmentname-buildpipeline)for your build pipeline with below rule.

```
ALL {resource.type = 'devopsbuildpipeline', resource.compartment.id = 'compartmentOCID'}

```
- Create dynamic group (EG: dg-compartmentname-deploymentpipeline)for your deployment pipeline with below rule.

```
All {resource.type = 'devopsdeploypipeline', resource.compartment.id = 'compartmentOCID'}
```

- Create dynamic group (Ef: dg-compartmentname-coderepo) for your coderepo with below rule.

```
ALL {resource.type = 'devopsrepository', resource.compartment.id = 'compartmentOCID'}
```

</details>

<details>
<summary>Devops deployment pipeline with OCI instances - Click to expand</summary>

- Create a dynamic group (Eg: dg-compartmentname-computeinstances) to group all the instances with below rule.

```
All {instance.compartment.id = 'compartmentOCID'}
```
</details>

<details>
<summary>Devops Connection - For external code repos (Github,Gitlab etc) - Click to expand</summary>

- Create a dynamic group (Eg: dg-compartmentname-devopsconnection) for devops connection with below rule.

```
ALL {resource.type = 'devopsconnection', resource.compartment.id = 'compartmentOCID'}
```

</details>

<details>
<summary>Use OCI functions with other OCI services (like use vault from functions etc) - Click to expand</summary>

- Create a dynamic group (Eg: dg-compartmentname-functions) to group all the instances with below rule.

```
resource.type = 'fnfunc'
resource.compartment.id = 'ocid1.compartment.oc1..xx'
```

</details>

<details>
<summary>Use OCI Gateway  with other OCI services (Functions etc) - Click to expand</summary>

- Create a dynamic group (Eg: dg-compartmentname-gateways) to group all the gateways with below rule.

```
ALL {resource.type = 'ApiGateway', resource.compartment.id = 'ocid1.compartment.oc1..xx'}
```

</details>


<!-- All about policies  -->

### ✔️ Policies 
<details>
<summary>OCI Users - Click to expand</summary>

| Use case | OCI Services  | Statement |
| :--- | :--- | :--- |
|Allow a specifc user group to manage devops services |User groups,Devops|```Allow group devops-admins to manage devops-family ```|

</details>

<details>
<summary>OCI Build pipeline - Click to expand</summary>

| Use case | OCI Services  | Statement |
| :--- | :--- | :--- |
| Deliver artifacts  with container registry from Build pipeline | Build pipeline , Container registry | ``` Allow dynamic-group dg-compartmentname-buildpipeline to manage repos in compartment <compartment_name> ``` |
|Use Vault or Personal Access token (GITHUB/GITLAB etc) with Build piepline |Build pipeline,Vault,Connection|```Allow dynamic-group dg-compartmentname-buildpipeline to read secret-family in compartment <compartment_name> ```|
|Use OCI Code repo or Invoke deployment from Build pipeline|Build pipeline,Cod repo,Deploy pipeline|```Allow dynamic-group dg-compartmentname-buildpipeline to manage devops-family in compartment <compartment_name> ```|
|Use Artifact repo with buildpipeline|Buildpipeline,Artifact registry|``` Allow dynamic-group dg-compartmentname-buildpipeline to manage generic-artifacts in compartment <compartment_name>```|
|Send notifications from buildpipeline|Build pipeline,Notification|```Allow dynamic-group dg-compartmentname-buildpipeline to use ons-topics in compartment <compartment_name> ```

</details>

<details>
<summary>OCI Deployment pipeline - Click to expand</summary>

| Use case | OCI Services  | Statement |
| :--- | :--- | :--- |
|Allow various resources (like VM/OKE etc) to use by deployment pipeline for deployments|Deployment pipeline,OCI resources|```Allow dynamic-group dg-compartmentname-deploymentpipeline to manage all-resources in compartment <compartment name> ```|
|Deploy application to instances|Deploy pipeline,Compute,Compute agents|```Allow dynamic-group dg-compartmentname-computeinstances to use instance-agent-command-execution-family in compartment <compartment_name>```;```Allow dynamic-group dg-compartmentname-computeinstances to read generic-artifacts in compartment <compartment_name> ```|
|Use artifacts from deployment pipeline|Deployment pipeline,Artifiact registry|```Allow dynamic-group dg-compartmentname-deploymentpipeline to read all-artifacts in compartment <compartment_name> ```


</details>
<details>
<summary>OCI Code repo & External repos - Click to expand</summary>

| Use case | OCI Services  | Statement |
| :--- | :--- | :--- |
|Use OCI code repo for oci devops|Code repo,Build pipeline|```Allow dynamic-group dg-compartmentname-coderepo to manage devops-family in compartment <compartment_name> ```|
|OCI Code repo to access resources with in the compartment|Code repo,OCI Resources|```Allow dynamic-group dg-compartmentname-coderepo to manage all-resources in tenancy ```|
|Allow external code repos(Github,Gitlab) connection via Personal Access Token(PAT)|Connection,Vault|```Allow dynamic-group dg-compartmentname-devopsconnection to read secret-family in compartment <compartment name>(Create this policy under tenancy's root) ```|

</details>

<details>
<summary>OCI functions - Click to expand</summary>

| Use case | OCI Services  | Statement |
| :--- | :--- | :--- |
|Use vault with OCI functions|Functions,Secrets|``` allow dynamic-group dg-compartmentname-functions to manage secret-family in compartment <compartment name>;allow dynamic-group dg-compartmentname-functions to manage vault in compartment <compartment name>;allow dynamic-group dg-compartmentname-functions to manage keys in compartment <compartment name> ```|
|Function read from repos for deployment|Functions,Repos|```Allow service FaaS to read repos in compartment <compartment name> ```|
|Function to manage resources|Function ,Resources|```Allo dynamic-group dg-compartmentname-functions to manage all-resources in compartment <compartment name> ```|
</details>

<details>
<summary>OCI gateway - Click to expand</summary>

| Use case | OCI Services  | Statement |
| :--- | :--- | :--- |
|Use gateway with Functions|Function,Gateway|``` Allow dynamic-group dg-compartmentname-gateway to use functions-family in compartment <compartment name> ```|
</details>

<!-- All about references -->

### 📕 References 

- Devops policies - OCI Documentation - [link](https://docs.oracle.com/en-us/iaas/Content/devops/using/devops_iampolicies.htm#devops_iam_policies) 

- Fine grained access to a specific component and actions - [link](https://docs.oracle.com/en-us/iaas/Content/devops/using/devops_iampolicies.htm#policy-details)