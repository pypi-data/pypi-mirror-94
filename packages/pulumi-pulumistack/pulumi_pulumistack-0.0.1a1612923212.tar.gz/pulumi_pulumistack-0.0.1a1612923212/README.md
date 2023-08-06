# pulumistack Pulumi Provider

A Pulumi provider for managing Pulumi `Stack`s.


## Build and Test

```bash
$ make ensure
$ make build
```

## Example

This example deploys an Azure Kubernetes Cluster (using a Go program that lives in `pulumi/examples`) and then a Guestbook application inside the Kubernetes cluster (using a C# program that also lives in a different folder of `pulumi/examples`).  These two stacks can be wired together based on config and outputs, and dependencies are tracked between the two stacks.

```ts
import * as pulumistack from "./pulumistack"
import * as pulumi from "@pulumi/pulumi";

const project = pulumi.getProject();
const stack = pulumi.getStack();

const cluster = new pulumistack.Stack("azure-go-aks", { 
    repoUrl: "https://github.com/pulumi/examples/",
    path: "azure-go-aks",
    name: `lukehoban/azure-go-aks/${project}-${stack}`,
    config: {
        "azure:location": "westus",
        "kubernetesVersion": "1.16.13",
    }
});

const app = new pulumistack.Stack("kubernetes-cs-guestbook", { 
    repoUrl: "https://github.com/pulumi/examples/",
    path: "kubernetes-cs-guestbook/components",
    name: `lukehoban/guestbook-csharp-components/${project}-${stack}`,
    config: {
        "kubernetes:kubeconfig": cluster.outputs["kubeconfig"],
    }
});

export const frontendIp = app.outputs["FrontendIp"];
```

Running `pulumi up` deploys each of the nested stacks and then the computed stack output.

```
$ pulumi up     
Previewing update (dev):
     Type                        Name                                Plan       
 +   pulumi:pulumi:Stack         pulumistack-kubeclussterandapp-dev  create     
 +   ├─ pulumistack:stack:Stack  azure-go-aks                        create     
 +   └─ pulumistack:stack:Stack  kubernetes-cs-guestbook             create     
 
Resources:
    + 3 to create

Do you want to perform this update? yes
Updating (dev):
     Type                        Name                                Status      
 +   pulumi:pulumi:Stack         pulumistack-kubeclussterandapp-dev  created     
 +   ├─ pulumistack:stack:Stack  azure-go-aks                        created     
 +   └─ pulumistack:stack:Stack  kubernetes-cs-guestbook             created     
 
Outputs:
    frontendIp: "13.87.216.164"

Resources:
    + 3 created

Duration: 7m41s

Permalink: https://app.pulumi.com/lukehoban/pulumistack-kubeclussterandapp/dev/updates/8
```

This results in a working Guestbook application running in the new AKS cluster:

```
$ curl 13.87.216.164
<html ng-app="redis">
  <head>
    <title>Guestbook</title>
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.2.12/angular.min.js"></script>
    <script src="controllers.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/angular-ui-bootstrap/0.13.0/ui-bootstrap-tpls.js"></script>
  </head>
  <body ng-controller="RedisCtrl">
    <div style="width: 50%; margin-left: 20px">
      <h2>Guestbook</h2>
    <form>
    <fieldset>
    <input ng-model="msg" placeholder="Messages" class="form-control" type="text" name="input"><br>
    <button type="button" class="btn btn-primary" ng-click="controller.onRedis()">Submit</button>
    </fieldset>
    </form>
    <div>
      <div ng-repeat="msg in messages track by $index">
        {{msg}}
      </div>
    </div>
    </div>
  </body>
</html>
```




## References

Other resoruces for learning about the Pulumi resource model:
* [Pulumi Kubernetes provider](https://github.com/pulumi/pulumi-kubernetes/blob/master/provider/pkg/provider/provider.go)
* [Pulumi Terraform Remote State provider](https://github.com/pulumi/pulumi-terraform/blob/master/provider/cmd/pulumi-resource-terraform/provider.go)
* [Dynamic Providers](https://www.pulumi.com/docs/intro/concepts/programming-model/#dynamicproviders)
