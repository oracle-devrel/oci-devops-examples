A sample illustration of helm based installation of OCI OKE,based on artifact upload.

----------


ℹ️   Summary of Interactions

- Use OCI Service connector hub and invoke a function when there will be  repository artifiact upload event occurs.

- The Function will intern deploy the artifiact using helm to the OCI OKE.

- The whole interaction is encompassed inside a private Virtual cloud network subnet.

Global flow diagram

---------

![](images/OCI_HELM_FUNCTION_ARTIFACT.png)

📗 Setup Dynamic groups 

-----------

1- A DG for functions .

rules 

```
resource.type = 'fnfunc'
resource.compartment.id = 'ocid1.compartment.oc1..xx'

```

![](images/dg_function.png)



2- A DG for Artifact repo.

rules

```
ALL {resource.type = 'artifactrepository', resource.compartment.id = 'ocid1.compartment.oc1..xx'}
```

![](images/dg_artifact.png)


📗 Setup Policies 

-----------

1 - Policy for function access OKE.

```
Allow dynamic-group <FUNCTION DG NAME> to manage cluster-family in compartment <COMPARTMENT NAME>
```

2 - Policy for function to read artifact.

```
Allow dynamic-group <FUNCTION DG NAME> to read all-artifacts in compartment <COMPARTMENT NAME>
```

3 - Policy to associate service connector hub and functions.

```
allow any-user to use fn-function in compartment id <COMPARTMENT OCID> where all {request.principal.type='serviceconnector', request.principal.compartment.id='<COMPARTMENT OCID>'}

```

```
allow any-user to use fn-invocation in compartment id <COMPARTMENT OCID> where all {request.principal.type= 'serviceconnector', request.principal.compartment.id='<COMPARTMENT OCID>'}
```

📗 Setup OCI Artifact Registry repo. 

-----------

- Create an Artifact registry repo.
- Select or unselect mutable artifact options according your needs.

![](images/oci_artifact.png)

- Make a note of the repo's OCID.


📗 Setup an OCI OKE. 

-----------

- Create an OCI OKE Cluster.
- Here we are using Quick create work flow ,you may use Custom one if you would like to create OKE with in your Private subnets.
- Ensure to select **Private Endpoint / Private Worker** ,you may  use Public one as well.

![](images/oci_oke_cluster.png)

![](images/oci_oke2.png)



📗 Update VCN.

-----------

- As we have used the **OKE Quick Create** work flow ,it will create VCN and associated compartments.Incase if you are using custom flow ,update your VCN with respective configurations [- reference](https://docs.oracle.com/en-us/iaas/Content/ContEng/Concepts/contengnetworkconfigexample.htm#example-privatek8sapi-privateworkers-publiclb). 

- We will be using the Private subnet used for OKE node to use for functions ,to be with in the same private network.To do so follow the below configurations .

-  Use VCN > OKE Specific VCN > Click on oke-nodesubnet > Edit the Security rule > Add an ingress rule .This would helm our jump host to access /function to allow helm and kubectl access.

![](images/vcn_subnets.png)


![](images/vcn_node_subnet_view.png)

![](images/vcn_subnet_node_secrule.png)



- Add an additional Ruting table entry to allow  the loadbalancer (we will be using public load balancer).To do so 

- Go to the VCN of OKE > Select Routing Table > Use Create Route Table 


![](images/vcn_rt1.png)

![](images/vcn_rt2.png)

- Click the route table , and add a new Route Rules.Select the target type as *Internet Gateway*,select the default Internetgateway created byt he OKE Quick create flow ,if not select the custom one which you have created along with OKE VCN setups.


![](images/vcn_rt3.png)



📗 Setup the Functions

-----------

- Create a function application,use the Private subnet of OKE nodesubet.Incase of custom OCI OKE flow , select possible private network with which the OKE and functions can communicate.

![](images/oci_fn1.png)

- Use the Application > Getting Started and setup the function context ,either on cloud shell or your local machine.

![](images/oci_fn2.png)

- Git clone and build the functions .

```
$ git clone https://github.com/RahulMR42/oci-helmdeploy-with-artifactrepo-and-functions
$ cd oci-helmdeploy-with-artifactrepo-and-functions
$ fn list apps (Valid the application name and context)
$ Update the func.yaml provide the region and oke cluster id.
$ fn deploy -v --app <FN APPLICATION NAME>
```

- Verify the functions via application > Functions view .


![](images/oci_fn3.png)

- Enable logs for the application via console.

![](images/oci_fn4.png)


📗 Setup OCI Service Connector Hub 

-----------

- Create a service connector hub connecting artifact update/upload event and the functions that we just created.
- Select the source as Logging and target as Functions 

![](images/sc1.png)

- In the configure source part ,select Artifact Registry and select the events are as Generic Artifact update /update by path and upload by path.

- Add an additional query and put data.request.path attribute with * <OCID of REP> *

- Add One more  additional filter ,select the Attribute as source and enter * sample-fastapi.zip * .Here we using a wildcard selection with a name ,which will be used as a target path while we will be uploading the helm artifacts to OCI artifacts repo. 

![](images/sc_basic

Or You may switch to Advance mode and paste the below query 

```
search "<OCID of OCI Compartment>/_Audit_Include_Subcompartment" | (type='com.oraclecloud.artifacts.updategenericartifactbypath' or type='com.oraclecloud.artifacts.putgenericartifactcontentbypath' or type='com.oraclecloud.artifacts.updategenericartifact') and (data.request.path='*<OCI of Artifact Repo>*') and (source='*sample-fastapi*')

```

![](images/sc_query.png)

- Skip configure Tasks.
- At the target section select the application and functions.

![](images/sc4.png)



📗 Create a Bastion and a Jump hosts (Optional)

-----------

- Create an instance , use the private subnet used for functions (OKENODE SUBNET)
- Ensure to enable Oracle Cloud agent at the time of creation .
    - Refer the document [here](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/manage-plugins.htm) and copy the inline script if the instance is not having an access to public yum repo.

    - Eg for Centos 8 as below,you can use the 'Show advanced option' and paste the inline script.

    ```

    #!/bin/sh
    cd ~
    curl -O https://objectstorage.us-phoenix-1.oraclecloud.com/p/-VOLFC0_me9TRHlsK9wLQihmRZe4-UjzinOrAvIORZhqZbPoH1P6cSocD1GFwvZW/n/imagegen/b/agents/o/oracle-cloud-agent-1.18.0-6194.el8.x86_64.rpm -v

    ```
    ![](images/oci_instance1.png)

- Ensure the bastion plugin is enabled (If not enable it) and ensure its in 'Running State'. It would take a while/2 - 5 mnts in the first time.

![](images/oc_instance2.png)


- Create an OCI bastion ,with this and the instance with Private network we will be able to check our OKE deployment using native commands.

![](images/oci_bastion1.png)

- Use the same subnet where we have function /instance and OKE node.

- Once the bastion is ready create a ssh port forwarding session.
    - Select the instance we created .
    - Add the correct ssh public key from a file or copy.

![](images/oci_bastion2.png)

- Once it became active , use the 3 dots and copy the SSH command .

- Go to your local machine from where we would want to establish the connection ,open a terminal and paste the SSH command.
- You should provide the correct path to your ssh private key.

![](images/local1.png)

- If the session is ok ,it would stay with out any output ,with out closing the terminal ,open another one on your local machine.

```
ssh -i oci_rsa -p <LOCAL PORT USED IN THE ABOVE COMMAND> opc@localhost
```

![](images/local2.png)

- Now you are in to the JUMP hosts.

-  Go back to the OCI OKE > Access Cluster and setup the machines 
- You need to install OCI CLI /follow the procedure and use the command given to get the access to OKE cluster.

![](images/oci_oke3.png)

![](images/local3.png)

- It would ask information while configuring OCI CLI and please provide those (Tenancy ID /User ID / Region etc)

- Install kubectl and helm using the official documentation.

    -   https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/ 
    -  Helm installation.

    ```
    export PATH=$PATH:/usr/local/bin; curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash; mv /usr/local/bin/helm /usr/bin/helm
    ```

- Try to access the OKE cluster and validate .
- Incase of an error ,check your VCN placement / CIDRs / OKE setups etc.

![](images/local5.png)


📗 Lets Test ..

-----------

- To do so use your local machine where you have OCI CLI & Helm installed or use OCI Cloud shell .

- Clone the sample application.

```
$ git clone https://github.com/RahulMR42/sample-python-app-with-helm-chart 
```

- Build docker image.

```
$ cd  sample-python-app-with-helm-chart
$ docker login <dtr url> (Provide credentials when prompted)
$ docker build -t <dockerurl/sample-python-app:<tag> .
$ docker push <dockerurl/sample-python-app:<tag>
```

- Update the values for helm chart.

```
$ vi helmchart/sample-fastapi-app/values.yaml

```

  -  Update below values 

  ```
  namespace
  image > repository:
  image > tag

  ```    

  - Create a helm package

  ```
  $ helm package helmchart/sample-fastapi-app
  ```

![](images/helm1.png)

- Now we will push to the artfact using OCI CLI.


```
oci artifacts generic artifact upload-by-path --repository-id <OCI Artifact Repo OCID> --artifact-path sample-fastapi.zip --artifact-version <VERSION in numbers > --content-body <PATH TO HELM PACKAGE>
```

- Ensure to use the same path name as that of  referred in the service connector query.

![](images/helm2.png)

- Ensure the upload is successfull via the artifact repo UI .

![](images/artifact_ui.png)



📗 Verify the outcome

-----------

- Validate this via the jump hosts using kubectl command.

![](images/kubect1.png)

- Validate the resources and fetch the loadbalancer IP to test the application.

![](images/kubectl2.png)

- You can validate the URL via browser as well ,as in this case we are using public loadbalancer (use http://<LoadBalanceIP>).

![](images/lb1.png)

- You can verify the function invokvation via the function application logs too .
- Use OCI Console >Applicatons >Logs >Loger name 

![](images/logs1.png)


🎵 Tail end

- You may use values from Vault as an input to functions and can use as an input to helm too.
- Dont forget to clean up the resources using helm delete <chart name> or kubectl delete <component>
- If you want to test again ,change the chart in the sample application ,do a helm packge and upload to artifact repo.
- You update the application via the python code (main.py) ,do a new docker build ,update the chart values.yaml image tag and upload too.



Contributors 
===========

- Author : Rahul M R.
- Colloboroators : NA
- Last release : Dec 2021


### Back to examples.
----

- 🍿 [Back to OCI Devops Deployment sample](./../README.md)
- 🏝️ [Back to OCI Devops sample](./../../README.md)

