# Typing a Helper Function

How I typed a helper function for interface key manipulation, highlighting the usage of `infer` to retrieve a part of a longer string literal type.

---

## Context

The [properties.ts](./properties.ts) file contains an interface which has properties with long key names (like `Octopus.Action.Kubernetes.WaitForJobs`). Those key names contain a common prefix, so ideally we should be composing the long key name from short names, which would make it easier for the user to access the property values, like this:

```ts
type ShortNames = {
    "ExecutionTimeout": number,
    "WaitForJobs": boolean,
    "DeploymentStyle": "Rolling" | "BlueGreen" | "Recreate"
}

type Properties = { 
    [key in keyof ShortNames as `Octopus.Action.Kubernetes.${key}`]: ShortNames[key] 
}
```

However, the [properties.ts](./properties.ts) file may not be editable (maybe in another package, or generated). Is there a way to still utilize the common prefix to save some typing (_pun intended_)? 

To do this, we need the `infer` keyword, which in this context can be seen as the inversion of the string literal conncatanation type. The implementation is in [index.ts](./index.ts).

---
[Home](../../../../../README.md)