# Using Oracle GraalVM in OCI DevOps Build Pipelines to build a Java App

This sample shows how to use `Oracle GraalVM` in `OCI DevOps build pipelines` to build a Java hello world application. You can use this approach to build any high performance Java application with Oracle GraalVM and OCI DevOps.

## What is GraalVM?

- GraalVM is a high performance JDK distribution that can accelerate any Java workload running on the HotSpot JVM.

- GraalVM Native Image ahead-of-time compilation enables you to build lightweight Java applications that are smaller, faster, and use less memory and CPU. At build time, GraalVM Native Image analyzes a Java application and its dependencies to identify just what classes, methods, and fields are necessary and generates optimized machine code for just those elements.

- Oracle GraalVM is available for use on Oracle Cloud Infrastructure (OCI) at no additional cost.



## Specific instruction to clone only this example.

   ```
   $ git init oci_devops_build_with_graalenterprise
   $ cd oci_devops_build_with_graalenterprise
   $ git remote add origin <url to this git repo>
   $ git config core. sparsecheckout true
   $ echo "oci-build-examples/oci_devops_build_with_graalenterprise/*">>.git/info/sparse-checkout
   $ git pull --depth=1 origin main

   ```

## Objectives

- Create an OCI build pipeline.
- Make a build using Oracle GraalVM.
- Here the focus will be on the build specification and DevOps build pipeline


## Procedure to use this illustration.

- Create an OCI notification topic - https://docs.oracle.com/en-us/iaas/Content/Notification/Tasks/managingtopicsandsubscriptions.htm#createTopic
- Create a DevOps project - https://docs.oracle.com/en-us/iaas/Content/devops/using/create_project.htm#create_a_project.
  Associate with the notification topic.

![](images/oci_devops_project.png)

- Enable logging for the DevOps project.

![](images/oci_devops_logs.png)

Create an OCI Dynamic group and add the below rules. Replace `<YOUR_COMPARMENT_OCID>` with your compartment OCID. - https://docs.cloud.oracle.com/iaas/Content/Identity/Tasks/managingdynamicgroups.htm

```markdown
ALL {resource.type = 'devopsbuildpipeline', resource.compartment.id = '<YOUR_COMPARMENT_OCID>'}

ALL {resource.type = 'devopsrepository', resource.compartment.id = '<YOUR_COMPARMENT_OCID>'}
```

- Create an OCI policy and add the following policy statements. Replace `<YOUR_DynamicGroup_NAME>` with the name of your dynamic group, and `<YOUR_COMPARTMENT_NAME>` with the name of your compartment. - https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policies.htm

```markdown
Allow dynamic-group <YOUR_DynamicGroup_NAME> to manage repos in compartment <YOUR_COMPARTMENT_NAME>
Allow dynamic-group  <YOUR_DynamicGroup_NAME> to use ons-topics in compartment <YOUR_COMPARTMENT_NAME>
```

- Switch back to OCI DevOps Project and create an OCI Code repo - https://docs.oracle.com/en-us/iaas/Content/devops/using/create_repo.htm#create_repo

![](images/oci_code_repo.png)

- Push the content to OCI Code repo - https://docs.oracle.com/en-us/iaas/Content/devops/using/clone_repo.htm

![](images/oci_coderepo_files.png)

- You may use other supported version control repos as well (like Github.com, Bitbucket.com, Bitbucket Cloud, etc.). You may also need to adjust the policies according to the connection and setup external connections accordingly - https://docs.oracle.com/en-us/iaas/Content/devops/using/create_connection.htm

- Create a new build pipeline. - https://docs.oracle.com/en-us/iaas/Content/devops/using/create_buildpipeline.htm

![](images/oci_buildpipeline.png)

- Use the `Add Stage` option and add a `Managed Build` stage to the build pipeline - https://docs.oracle.com/en-us/iaas/Content/devops/using/add_buildstage.htm

![](images/oci_buildpipeline_managedbuild.png)

- Click `Next` and provide the details.
- In the `Build spec file path`, enter `build_spec.yaml` to use the [GraalVM Enterprise 22.x Java 17 build spec](build_spec.yaml). Alternatively, you can enter `build_spec_oracle_graalvm_jdk17.yaml` to use the [Oracle GraalVM for JDK 17 build spec](./build_spec_oracle_graalvm_jdk17.yaml) or `build_spec_oracle_graalvm_jdk20.yaml` to use the [Oracle GraalVM for JDK 20 build spec](./build_spec_oracle_graalvm_jdk20.yaml).

![](images/oci_buildstage_1.png)

- Associate the Primary code repository with the code repo containing the actual code.

![](images/oci_build_coderepo.png)

- Click `Add` and add the stage.

![](images/oci_buildpipelinestages.png)


## Take a closer look at the build instructions below

To install and use Oracle GraalVM in the DevOps build pipeline, the build specification file is as follows:

1. Add the following command to install the required Oracle GraalVM components. For example, this command installs Native Image along with the Java Development Kit (JDK) and other necessary dependencies.

    ```shell
    steps:
      - type: Command
        name: "Install Oracle GraalVM Enterprise 22.x Native Image for Java17"
        command: |
          yum -y install graalvm22-ee-17-native-image
    ```

2. Set the JAVA_HOME environment variable.

    ```shell
    env:
      variables:
        "JAVA_HOME" : "/usr/lib64/graalvm/graalvm22-ee-java17"
    ```

3. Set the PATH environment variable.

    ```shell
    env:
      variables:
        # PATH is a reserved variable and cannot be defined as a variable.
        # PATH can be changed in a build step and the change is visible in subsequent steps.
    
    steps:
      - type: Command
        name: "Set PATH Variable"
        command: |
          export PATH=$JAVA_HOME/bin:$PATH
    ```

4. Build a native executable for your Java application.

    ```shell
    steps:
      - type: Command
        name: "Build a native executable"
        command: |
          mvn --no-transfer-progress -Pnative -DskipTests package
    ```

5. The executable file can be found under `target/my-app`.

```markdown
  - name: app_native_executable
    type: BINARY
    location: target/my-app
```

Here's the complete [build specification for GraalVM Enterprise 22.x Java 17](build_spec.yaml) file. Alternatively, you can use the 
[build specification for Oracle GraalVM for JDK 17](./build_spec_oracle_graalvm_jdk17.yaml) or
[build specification for Oracle GraalVM for JDK 20](./build_spec_oracle_graalvm_jdk20.yaml).


## How to export the executable file outside of the build pipeline stage.

The following instructions will help you to export the `executable app file` to OCI Artifactory and which can then be used in the further stage including deployment pipelines.

- Create an OCI artifact registry. https://docs.oracle.com/en-us/iaas/Content/artifacts/home.htm

![](images/oci_artifact_registry.png)

- Switch back to `DevOps Project` and create an `Artifact`- https://docs.oracle.com/en-us/iaas/Content/devops/using/artifacts.htm

- Select the type as `General artifact`

![](images/oci_devops_artifact_1.png)

- Select the `Artifact source` as the Artifact Registry repository. Use `Select` and associate with the artifact registry created.

![](images/oci_devops_artifact_2.png)


- Use option `Set Custom Location` as Artifact location.
- Provide a path and version as `${BUILDRUN_HASH}`, this is to maintain immutable artifacts.
- The variable `BUILDRUN_HASH` is derived during managed build stage and exported as an exportedVariables.You may use any other name ,but ensure to update the file [build_spec.yaml](build_spec.yaml).
- Select `Yes, substitute placeholders` as an option and click `Add`.

![](images/oci_devops_artifact_3.png)

- Under `Build pipeline` use the `+` icon after the current stage and add a new stage named `Deliver artifacts`

![](images/oci_build_deliverartifact.png)

- Associate it with the `DevOps Artifact` created.

![](images/oci_uploadartifact_reference.png)


- Use `app_native_executable` result artifact name.
- The name `app_native_executable` is a reference to the outputArtifact defined under the the file [build_spec.yaml](build_spec.yaml).
- Click `Add` and add the stage.

![](images/oci_upload_artifact.png)


- The build pipeline with two stages would look like the one below.

![](images/oci_buidpipeline_all_stages.png)


## Let's test.

- Use `Start manual run` under OCI Buildpipeline and run the pipeline stages.

![](images/oci_build_startmanual_run.png)

- Wait for all the stages to complete
  ![](images/oci_buildstages_inprogress.png)

![](images/oci_buildstages_done.png)

- You should see a new artfact under the `Artifact registry repo` created earlier.

![](images/oci_artifact.png)

- The exported executable can be used on any of the supporting infrastructures to execute or can use to deploy via `OCI deployment pipeline` to compute, container or function resources.

## Optional - Run build with more verbose output.

- An additional build instruction file as [build_spec_verbose.yaml](build_spec_verbose.yaml)
  can be used for more verbose output with the managed build.
- To do so, switch to `OCI DevOps project` > `OCI Build pipeline ` > Click `3 dots` on the `Managed Build` stage and click on `View details` and then `Edit Stage`.

![](images/oci_buildstage_details.png)

- Change  `Build spec file path` as `build_spec_verbose.yaml`  and `Save changes`

![](images/oci_buildspec_verbose.png)

- Do another manual run for the build pipeline and you will see more verbose build logs.

## Sample Build Logs

1. The `yum install` build log statements should be similar to:

    ```shell
    ...
    EXEC: Installed:   
    EXEC:   graalvm22-ee-17-native-image.x86_64 0:22.1.0.1-1.el7                             
    EXEC:    
    EXEC: Dependency Installed:   
    EXEC:   glibc-static.x86_64 0:2.17-326.0.1.el7_9                                         
    EXEC:   graalvm22-ee-17-jdk.x86_64 0:22.1.0.1-1.el7                                      
    EXEC:   libstdc++-static.x86_64 0:4.8.5-44.0.3.el7                                       
    EXEC:   zlib-static.x86_64 0:1.2.7-20.el7_9                                              
    EXEC:    
    EXEC: Complete!
    ...
    ```

2. The native executable build log statements should be similar to:

    ```shell
    ...
    EXEC: ==================================================================
    EXEC: GraalVM Native Image: Generating 'my-app' (executable)...   
    EXEC: ==================================================================
    EXEC: [1/7] Initializing...                     (5.6s @ 0.11GB)   
    EXEC:  Version info: 'GraalVM 22.1.0.1 Java 17 EE'   
    EXEC:  C compiler: gcc (redhat, x86_64, 4.8.5)   
    EXEC:  Garbage collector: Serial GC   
    EXEC: [2/7] Performing analysis...  [******]    (9.5s @ 0.32GB)   
    EXEC:    1,880 (62.46%) of  3,010 classes reachable   
    EXEC:    1,684 (46.71%) of  3,605 fields reachable   
    EXEC:    7,784 (36.98%) of 21,049 methods reachable   
    EXEC:       21 classes,     0 fields, and   285 methods registered for reflection   
    EXEC:       48 classes,    32 fields, and    47 methods registered for JNI access   
    EXEC: [3/7] Building universe...                (1.1s @ 0.45GB)   
    EXEC: [4/7] Parsing methods...      [*]         (0.8s @ 0.58GB)   
    EXEC: [5/7] Inlining methods...     [****]      (1.2s @ 0.97GB)   
    EXEC: [6/7] Compiling methods...    [*****]     (21.2s @ 0.75GB)   
    EXEC: [7/7] Creating image...                   (0.9s @ 0.92GB)   
    EXEC:    2.62MB (46.31%) for code area:    3,708 compilation units   
    EXEC:    2.45MB (43.34%) for image heap:     945 classes and 38,518 objects   
    EXEC:  600.06KB (10.35%) for other data   
    EXEC:    5.66MB in total   
    EXEC: ------------------------------------------------------------------
    ...
    EXEC: ------------------------------------------------------------------
    EXEC: 0.9s (2.1% of total time) in 18 GCs | Peak RSS: 2.44GB | CPU load: 3.41   
    EXEC: ------------------------------------------------------------------
    EXEC: Produced artifacts:   
    EXEC:  /workspace/gvmee-yum/target/my-app (executable)   
    EXEC:  /workspace/gvmee-yum/target/my-app.build_artifacts.txt   
    EXEC: ==================================================================
    EXEC: Finished generating 'my-app' in 41.7s.   
    ...
    ```

References
==========

- Using Oracle GraalVM in DevOps Build Pipelines - https://docs.oracle.com/en-us/iaas/Content/devops/using/graalvm.htm
- Oracle Cloud Infrastructure DevOps - https://docs.oracle.com/en-us/iaas/Content/devops/using/home.htm
- Oracle GraalVM - https://www.oracle.com/java/graalvm/

Contributors
===========

- Author: [Rahul M R](https://github.com/RahulMR42).
- Collaborators: [Sachin Pikle](https://github.com/sachin-pikle)
- Last release: July 2022

### Back to examples.
----

- 🍿 [Back to OCI DevOps Build sample](./../README.md)
- 🏝️ [Back to OCI Devops sample](./../../README.md)



