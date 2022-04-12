
A sample illustration of [Github](https://github.com/) code repo integration with OCI Devops.

--------

#### Objectives

- Create a sample repo and personal access token via Github.
- Create vault ,policies as accordingly.
- Create a devops connection and integrate with OCI.
- Test and validate the integrations.

* Specific instruction to clone only this example.

    ```
    $ git init oci-devops-coderepo-with-github
    $ cd oci-devops-coderepo-with-github
    $ git remote add origin https://github.com/oracle-devrel/oci-devops-examples
    $ git config core.sparsecheckout true
    $ echo "oci-coderepo-examples/oci-devops-coderepo-with-github/*">>.git/info/sparse-checkout
    $ git pull --depth=1 origin main

    ```

#### Procedure 

- Follow Github documentation and do a sign in. - http://github.com 
- Create a Github  repo (it can be public or private)  - https://docs.github.com/en/get-started/quickstart/create-a-repo

![](images/github-create-new-repo.png)

- Click on the Gitlab profile icon  and select `Settings` option.

![](images/github-settings.png)

- Click `Developer Settings`

![](images/github-devsettings.png)

- Click `Personal Access Token` > `Generate Token`

![](images/github-pat.png)

- Provide a name and select one of the below scope .

    - `repo` ( Full control of private repositories) for private and public repo access.
    - `public_repo` (For public repo access only). 

![](images/github-repo-1.png)

- Please make a note of the newly generated token.

- In order to security store and orchestrate Gitlab Personal Access token , we will create a new OCI Vault for now .

-  Create a new vault under the concerned compartment. - https://docs.oracle.com/en-us/iaas/Content/KeyManagement/Concepts/keyoverview.htm#Overview_of_Vault 

![](images/oci-vault-create.png)

![](images/oci-vault-create-1.png)

- Create a new `Encryption Key`.

![](images/oci-vault-create-2.png)

- Create a new secrets and store the Github - PAT.

![](images/oci-vault-3.png)

- Create a `Dynamic group` with below rules .

```
ALL {resource.type = 'devopsconnection', resource.compartment.id = 'ocid1.compartment.oc1..xxxxx'}
```

![](images/oci-dg.png)

- Create a policy (Ensure to create it under the **ROOT of tenancy**) for the dynamic groups with below policy statement.

```
Allow dynamic-group mr-devops-policy-checker-dg-connection to read secret-family in compartment <compartment name>

```

![](images/oci-policy.png)

- Create a notification topic ,that will be used for devops - https://docs.oracle.com/en-us/iaas/Content/Notification/Tasks/managingtopicsandsubscriptions.htm#createTopic

![](images/oci-notifications.png)

- Create a devops project - https://docs.oracle.com/en-us/iaas/Content/devops/using/create_project.htm#create_a_project

- Ensure to associate it with a `notification topic`.

![](images/oci-devops-projects.png)

- Under the project click `Enable Logging` and `toggle`  and enable the logs.

![](images/oci-logs.png)

![](images/oci-logs-1.png)

- Select the logging details and enable .

![](images/oci-logs-2.png)

![](images/oci-logs-3.png)

- Create a new  `external connection` - https://docs.oracle.com/en-us/iaas/Content/devops/using/create_connection.htm

![](images/oci-ec1.png)

 - Select the type as `Github`  and associate with the Vault and secret created.

 ![](images/oci-github-ec1.png)

- Use devops `Code Repositories` and mirror external repo to oci devops. - https://docs.oracle.com/en-us/iaas/Content/devops/using/mirror_repo.htm 

![](images/oci-repo.png)

- Select the external connection created and select the Gitlab repository. You may mention a custom name (as optional) which will be used when the external repo is cloned to OCI Code repo.

- You may alter the Scheduling type to a custom value if needed .The default sync interval is  `15 minutes`.

![](images/oci-mirror-2.png)

- After a while the repo will be available via `OCI Code Repo`

![](images/oci-coderepo-github-mirror.png)

- You may use the options and `Re synchronize` if needed.

![](images/oci-repo-mirror-options.png)

Contributors 
===========

- Author : Rahul M R.
- Collaborators : NA
- Last release : Apr 2022

### Back to examples.
----

- 🍿 [Back to OCI Devops Coderepo sample](./../README.md)
- 🏝️ [Back to OCI Devops sample](./../../README.md)


