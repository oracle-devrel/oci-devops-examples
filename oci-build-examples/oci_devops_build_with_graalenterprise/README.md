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
- In the `Build spec file path`, enter `build_spec_oracle_graalvm_jdk21.yaml` to use [Oracle GraalVM for JDK 21](./build_spec_oracle_graalvm_jdk21.yaml) or `build_spec_oracle_graalvm_jdk17.yaml` to use [Oracle GraalVM for JDK 17](./build_spec_oracle_graalvm_jdk17.yaml). Alternatively, you can enter `build_spec.yaml` to use the legacy [GraalVM Enterprise 22.x Java 17](build_spec.yaml). 

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
        name: "Install Oracle GraalVM for JDK 21 (Native Image and JDK)"
        command: |
          yum -y install graalvm-21-native-image
    ```

2. Set the JAVA_HOME environment variable.

    ```shell
    env:
      variables:
        "JAVA_HOME" : "/usr/lib64/graalvm/graalvm-java21"
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

Here's the complete [build specification for Oracle GraalVM for JDK 21](./build_spec_oracle_graalvm_jdk21.yaml). Alternatively, you can use the [build specification for Oracle GraalVM for JDK 17](./build_spec_oracle_graalvm_jdk17.yaml) or the legacy [build specification for GraalVM Enterprise 22.x Java 17](build_spec.yaml) file. 


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
- The variable `BUILDRUN_HASH` is derived during managed build stage and exported as an exportedVariables.You may use any other name, but ensure to update the corresponding build specification file.
- Select `Yes, substitute placeholders` as an option and click `Add`.

![](images/oci_devops_artifact_3.png)

- Under `Build pipeline` use the `+` icon after the current stage and add a new stage named `Deliver artifacts`

![](images/oci_build_deliverartifact.png)

- Associate it with the `DevOps Artifact` created.

![](images/oci_uploadartifact_reference.png)


- Use `app_native_executable` result artifact name.
- The name `app_native_executable` is a reference to the outputArtifact defined under the corresponding build specification file.
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
    EXEC:   graalvm-21-native-image.x86_64 0:21.0.7-1.el7                                    
    EXEC:    
    EXEC: Dependency Installed:   
    EXEC:   glibc-static.x86_64 0:2.17-326.0.9.el7_9.3                                       
    EXEC:   graalvm-21-jdk.x86_64 0:21.0.7-1.el7                                             
    EXEC:   libstdc++-static.x86_64 0:4.8.5-44.0.3.el7                                       
    EXEC:   zlib-static.x86_64 0:1.2.7-21.el7_9                                              
    EXEC:    
    EXEC: Dependency Updated:   
    EXEC:   glibc.x86_64 0:2.17-326.0.9.el7_9.3                                              
    EXEC:   glibc-common.x86_64 0:2.17-326.0.9.el7_9.3                                       
    EXEC:   glibc-devel.x86_64 0:2.17-326.0.9.el7_9.3                                        
    EXEC:   glibc-headers.x86_64 0:2.17-326.0.9.el7_9.3                                      
    EXEC:    
    EXEC: Complete!   
    ...
    ```

2. The native executable build log statements should be similar to:

    ```shell
    ...
    EXEC: ========================================================================================================================   
    EXEC: GraalVM Native Image: Generating 'my-app' (executable)...   
    EXEC: ========================================================================================================================   
    EXEC: For detailed information and explanations on the build output, visit:   
    EXEC: https://github.com/oracle/graal/blob/master/docs/reference-manual/native-image/BuildOutput.md   
    EXEC: ------------------------------------------------------------------------------------------------------------------------   
    EXEC: [1/8] Initializing...                                                                                    (3.6s @ 0.09GB)   
    EXEC:  Java version: 21.0.7+8-LTS, vendor version: Oracle GraalVM 21.0.7+8.1   
    EXEC:  Graal compiler: optimization level: 2, target machine: x86-64-v3, PGO: ML-inferred   
    EXEC:  C compiler: gcc (redhat, x86_64, 4.8.5)   
    EXEC:  Garbage collector: Serial GC (max heap size: 80% of RAM)   
    EXEC:  1 user-specific feature(s):   
    EXEC:  - com.oracle.svm.thirdparty.gson.GsonFeature   
    EXEC: ------------------------------------------------------------------------------------------------------------------------   
    EXEC: Build resources:   
    EXEC:  - 5.11GB of memory (75.6% of 6.76GB system memory, determined at start)   
    EXEC:  - 4 thread(s) (100.0% of 4 available processor(s), determined at start)   
    EXEC: [2/8] Performing analysis...  [*****]                                                                    (8.5s @ 0.19GB)   
    EXEC:     2,052 reachable types   (60.0% of    3,421 total)   
    EXEC:     1,935 reachable fields  (45.3% of    4,272 total)   
    EXEC:     8,767 reachable methods (36.2% of   24,223 total)   
    EXEC:       741 types,    37 fields, and   332 methods registered for reflection   
    EXEC:        49 types,    33 fields, and    48 methods registered for JNI access   
    EXEC:         4 native libraries: dl, pthread, rt, z   
    EXEC: [3/8] Building universe...                                                                               (1.5s @ 0.23GB)   
    EXEC: [4/8] Parsing methods...      [**]                                                                       (2.7s @ 0.23GB)   
    EXEC: [5/8] Inlining methods...     [***]                                                                      (0.8s @ 0.24GB)   
    EXEC: [6/8] Compiling methods...    [****]                                                                    (17.1s @ 0.27GB)   
    EXEC: [7/8] Laying out methods...   [*]                                                                        (0.7s @ 0.26GB)   
    EXEC: [8/8] Creating image...       [*]                                                                        (1.1s @ 0.23GB)   
    EXEC:    2.82MB (42.58%) for code area:     3,945 compilation units   
    EXEC:    3.18MB (48.04%) for image heap:   53,077 objects and 43 resources   
    EXEC:  636.31kB ( 9.39%) for other data   
    EXEC:    6.62MB in total   
    EXEC: ------------------------------------------------------------------------------------------------------------------------   
    EXEC: Top 10 origins of code area:                                Top 10 object types in image heap:   
    EXEC:    1.41MB java.base                                          765.27kB byte[] for code metadata   
    EXEC:    1.12MB svm.jar (Native Image)                             693.88kB byte[] for java.lang.String   
    EXEC:   84.35kB com.oracle.svm.svm_enterprise                      363.73kB java.lang.String   
    EXEC:   42.24kB jdk.proxy2                                         322.13kB java.lang.Class   
    EXEC:   37.79kB jdk.proxy1                                         168.13kB java.util.HashMap$Node   
    EXEC:   30.20kB org.graalvm.nativeimage.base                       114.01kB char[]   
    EXEC:   27.42kB org.graalvm.collections                             94.77kB heap alignment   
    EXEC:   21.20kB jdk.internal.vm.ci                                  81.83kB java.lang.Object[]   
    EXEC:   16.79kB jdk.internal.vm.compiler                            81.45kB byte[] for reflection metadata   
    EXEC:   11.80kB jdk.proxy3                                          80.16kB com.oracle.svm.core.hub.DynamicHubCompanion   
    EXEC:   389.00B for 1 more packages                                490.66kB for 523 more object types   
    EXEC:                               Use '-H:+BuildReport' to create a report with more details.   
    EXEC: ------------------------------------------------------------------------------------------------------------------------   
    EXEC: Security report:   
    EXEC:  - Binary does not include Java deserialization.   
    EXEC:  - Use '--enable-sbom' to embed a Software Bill of Materials (SBOM) in the binary.   
    EXEC: ------------------------------------------------------------------------------------------------------------------------   
    EXEC: Recommendations:   
    EXEC:  G1GC: Use the G1 GC ('--gc=G1') for improved latency and throughput.   
    EXEC:  PGO:  Use Profile-Guided Optimizations ('--pgo') for improved throughput.   
    EXEC:  INIT: Adopt '--strict-image-heap' to prepare for the next GraalVM release.   
    EXEC:  HEAP: Set max heap for improved and more predictable memory usage.   
    EXEC:  CPU:  Enable more CPU features with '-march=native' for improved performance.   
    EXEC: ------------------------------------------------------------------------------------------------------------------------   
    EXEC:                         2.8s (7.5% of total time) in 262 GCs | Peak RSS: 0.79GB | CPU load: 3.27   
    EXEC: ------------------------------------------------------------------------------------------------------------------------   
    EXEC: Produced artifacts:   
    EXEC:  /workspace/gvmee-yum/target/my-app (executable)   
    EXEC: ========================================================================================================================   
    EXEC: Finished generating 'my-app' in 36.7s.   
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
- Last updated: July 2025

### Back to examples.
----

- 🍿 [Back to OCI DevOps Build sample](./../README.md)
- 🏝️ [Back to OCI Devops sample](./../../README.md)



