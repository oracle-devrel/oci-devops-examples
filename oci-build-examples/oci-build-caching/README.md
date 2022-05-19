# OCI DevOps - Speed up builds with caching

In most cases, the build time is consumed in downloading or preparing certain build dependancies like maven dependencies, node_modules, pip dependancies, etc... This procedure talks about on how to reduce time by caching those dependencies for the subsequent runs. 

In this way, the first run would take full time to download and setup build dependancies. But the subsequent runs will be more efficient through the cache.

For this, sample java maven-based application is used to demonstrate build caching.

### Prerequisites/Assumptions
* Assumed you are already familiar with OCI DevOps. Please refer [Documentation](https://www.oracle.com/devops/devops-service/)
* To know how to run the this maven project in your local. Please refer [this](./SETUP-PROJECT.md)
* Assumed that you are using docker build inside your `build_spec.yaml`
* As OCI Object storage is used to store the cache, Please create a bucket and set right access policies for the same. [Click here](https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/objectstorageoverview.htm) to know more about Object Storage.

### References
* [OCI DevOps CICD Reference Architecture](https://docs.oracle.com/en/solutions/ci-cd-pipe-oci-devops/index.html)
* [OCI DevOps Documentation](https://docs.oracle.com/en-us/iaas/Content/devops/using/home.htm)
* [Creating DevOps Project](https://docs.oracle.com/en-us/iaas/Content/devops/using/create_project.htm)
* [Creating Repository](https://docs.oracle.com/en-us/iaas/Content/devops/using/managing_coderepo.htm)
* [Creating Build Pipeline](https://docs.oracle.com/en-us/iaas/Content/devops/using/managing_build_pipelines.htm)
* [Creating Deploy Pipeline](https://docs.oracle.com/en-us/iaas/Content/devops/using/deployment_pipelines.htm)


### Overview of Changes
For any project, you may tweek `build_spec.yaml` to enable build cache.

#### Step 1
* Create OCI Object Storage bucket `build-cache`
* Create Policies, for build to access Object Storage bucket.
```
Allow dynamic-group <dg-devops-build-pipeline> to read buckets in compartment <compartment-name>

Allow dynamic-group <dg-devops-build-pipeline> to manage objects in compartment <compartment-name> where all {target.bucket.name='build-cache'}
```

#### Step 2
Docker BuildKit is installed to enable few advanced docker build commands for caching.
```
  - type: Command
    name: "Docker BuildKit Setup"
    timeoutInSeconds: 140
    command: |
      wget https://github.com/docker/buildx/releases/download/v0.8.2/buildx-v0.8.2.linux-amd64 -O docker-buildx
      mkdir -p ~/.docker/cli-plugins
      mv docker-buildx ~/.docker/cli-plugins/
      chmod +x ~/.docker/cli-plugins/docker-buildx
      docker buildx install
```
#### Step 3
`Build Cache Restore` stage is used to download the pre-uploaded cache from OCI Object Storage.

```
  - type: Command
    name: "Build Cache Restore"
    timeoutInSeconds: 140
    command: |
      oci os object get --bucket-name build-cache --file ${BUILD_CACHE_OS_FILE_NAME} --name ${BUILD_CACHE_OS_FILE_NAME} && unzip ${BUILD_CACHE_OS_FILE_NAME}
      echo "Done..."
```

#### Step 4
In actual build stage, below comands are used in the place of regular `docker build`.
```
  - type: Command
    name: "Docker build"
    command: |
      export DOCKER_BUILDKIT=1
      export DOCKER_CLI_EXPERIMENTAL=enabled
      docker buildx create --use
      docker buildx build -t="hello-world-java" --cache-from=type=local,src=./cache --cache-to=type=local,dest=./cache --load .
      echo "DONE"
```

#### Step 5
`Build Cache Upload` stage is added to collect the generated build cache and upload to OCI Object Storage bucket. This is used for subsequent builds.

```
  - type: Command
    name: "Build Cache Upload"
    timeoutInSeconds: 140
    command: |
      rm ${BUILD_CACHE_OS_FILE_NAME} && zip -r ${BUILD_CACHE_OS_FILE_NAME} cache/*
      oci os object put --bucket-name build-cache --file ${BUILD_CACHE_OS_FILE_NAME} --force
```

#### Step 6
In `Dockerfile`, We need to pass `--mount` argument to `RUN` command to use cache for the specific build command as below.

```
RUN --mount=type=cache,target=/root/.m2 mvn package
```

### Results

#### Before OCI Build Cache
![6m 33s](images/BeforeOCIBuildCache.png "Before Caching")

#### After OCI Build Cache
![0m 49s](images/AfterOCIBuildCache.png "After Caching")

### Contributors 

- Author : Ashok CM
- Collaborators : NA
- Last release : May 2022

