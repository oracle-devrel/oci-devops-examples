# oci-devops-examples

[![License: UPL](https://img.shields.io/badge/license-UPL-green)](https://img.shields.io/badge/license-UPL-green) 


## Introduction

Rapid delivery of software is essential for efficiently running your applications in the cloud. Oracle DevOps service provides a continuous integration and deployment (CI/CD) platform for developers. You can use the OCI DevOps service to easily build, test, and deploy software and applications on Oracle Cloud. DevOps build and deployment pipelines reduce change-driven errors and decrease the time customers spend on building and deploying releases.

The service also provides private Git repositories to store your code and it supports connections to external code repositories. Whether you're migrating workloads to Oracle Cloud Infrastructure (OCI)—from on-premises or other clouds—or developing new applications on OCI, you can use the DevOps service to simplify your software delivery lifecycle.

## OCI Devops examples (Catogorical view )

- [⚡ CICD with OCI Devops services - samples](./oci-pipeline-examples/README.md)         
- [⚡ OCI Devops Build service - samples](./oci-build-examples/README.md) 
- [⚡ OCI Devops Deployment service - samples](./oci-deployment-examples/README.md) 
- [⚡ OCI Source Code Management service - sample](./oci-coderepo-examples/README.md)
- [⚡ OCI Devops Projects,Policies and Groups - sample](./oci-config-examples/README.md)

### Latest samples 

- 🛎️[Sample illustration of OCI DevOps deployment pipeline with DevOps Deploy Shell stage.]( https://github.com/oracle-devrel/oci-devops-examples/blob/main/oci-deployment-examples/oci-deployment-shell-stages)
- 🛎️[A sample to run OCI AI Anomaly detection from OCI Build-pipeline.](https://github.com/oracle-devrel/oci-devops-examples/tree/main/oci-build-examples/oci-devops-anomaly-detection)
- 🛎️[A way (workaround) to execute commands on to a Windows machine using OCI Run command agent from OCI Build pipeline.](https://github.com/oracle-devrel/oci-devops-examples/tree/main/oci-build-examples/oci-devops-connect-to-windows-from-buildmachines)
- 🛎[Sample illustration of OCI DevOps deployment pipeline with stage level paramters.]( https://github.com/oracle-devrel/oci-devops-examples/blob/main/oci-deployment-examples/oci-deployment-stagelevelparams)

## All samples (A to Z sorted order)

- [🌟 All the published samples of OCI-devops](AIO.md)

## Instruction to clone a specific example.

```
    $ git init <foldername> 
    $ cd <Foldername> 
    $ git remote add origin <url to this git repo>
    $ git config core.sparsecheckout true
    $ echo "example path/*">>.git/info/sparse-checkout
    $ git pull --depth=1 origin main
```

A sample to clone a build-sample with oci sonarqube integration.

    $ git init oci_devops_sonarqube
    $ cd oci_devops_sonarqube
    $ git remote add origin <url to this git repo>
    $ git config core.sparsecheckout true
    $ echo "oci-build-examples/oci_buildrunner_with_sonarqube/*">>.git/info/sparse-checkout
    $ git pull --depth=1 origin main
    $ ls -ltr */*
    $ ls -ltr */*
            -rw-r--r--  1 rahulmr_in  staff   202 Feb 22 14:33 oci_buildrunner_with_sonarqube/Dockerfile
            -rw-r--r--  1 rahulmr_in  staff  6313 Feb 22 14:33 oci_buildrunner_with_sonarqube/README.md
            -rwxr-xr-x  1 rahulmr_in  staff    41 Feb 22 14:33 oci_buildrunner_with_sonarqube/build.sh
            -rw-r--r--  1 rahulmr_in  staff  3204 Feb 22 14:33 oci_buildrunner_with_sonarqube/build_spec.yaml
            -rw-r--r--  1 rahulmr_in  staff  1011 Feb 22 14:33 oci_buildrunner_with_sonarqube/deploy_spec.yaml
            -rw-r--r--  1 rahulmr_in  staff    53 Feb 22 14:33 oci_buildrunner_with_sonarqube/package.json
            -rwxr-xr-x  1 rahulmr_in  staff    77 Feb 22 14:33 oci_buildrunner_with_sonarqube/run.sh
            -rw-r--r--  1 rahulmr_in  staff  2901 Feb 22 14:33 oci_buildrunner_with_sonarqube/server.js

            oci_buildrunner_with_sonarqube/images:
            total 3136
            .....

## Contributing
This project is open source.  Please submit your contributions by forking this repository and submitting a pull request!  Oracle appreciates any contributions that are made by the open source community.

## License
Copyright (c) 2022 Oracle and/or its affiliates.

Licensed under the Universal Permissive License (UPL), Version 1.0.

See [LICENSE](LICENSE) for more details.

ORACLE AND ITS AFFILIATES DO NOT PROVIDE ANY WARRANTY WHATSOEVER, EXPRESS OR IMPLIED, FOR ANY SOFTWARE, MATERIAL OR CONTENT OF ANY KIND CONTAINED OR PRODUCED WITHIN THIS REPOSITORY, AND IN PARTICULAR SPECIFICALLY DISCLAIM ANY AND ALL IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.  FURTHERMORE, ORACLE AND ITS AFFILIATES DO NOT REPRESENT THAT ANY CUSTOMARY SECURITY REVIEW HAS BEEN PERFORMED WITH RESPECT TO ANY SOFTWARE, MATERIAL OR CONTENT CONTAINED OR PRODUCED WITHIN THIS REPOSITORY. IN ADDITION, AND WITHOUT LIMITING THE FOREGOING, THIRD PARTIES MAY HAVE POSTED SOFTWARE, MATERIAL OR CONTENT TO THIS REPOSITORY WITHOUT ANY REVIEW. USE AT YOUR OWN RISK. 
