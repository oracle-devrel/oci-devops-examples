<details>
<summary>

```yaml
version: 0.1
component: command
timeoutInSeconds: 10000
shell: bash
failImmediatelyOnError: true
env:
  variables:
    NAMESPACE: "ns-demo"
inputArtifacts:
  - name: sample-kube-yaml
    type: URL
    url: https://raw.githubusercontent.com/kubernetes/website/main/content/en/examples/application/deployment.yaml
    location: ${OCI_WORKSPACE_DIR}/ngnix.yaml

steps:
  - type: Command
    timeoutInSeconds: 600
    name: "stepOne"
    command: |
      echo "Step One.."
      ls -ltr 

    onFailure:
      - type: Command
        command: |
          echo "Handled Failure for Step One"
        timeoutInSeconds: 40
        
  - type: Command
    timeoutInSeconds: 600
    name: "stepTwo"
    command: |
      echo "Step two"
      ls -ltr 

    onFailure:
      - type: Command
        command: |
          echo "Handled Failure for Step One"
        timeoutInSeconds: 40
```
</summary>

</details>