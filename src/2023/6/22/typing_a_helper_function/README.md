# Typing a Helper Function

How I typed a helper function for interface key manipulation, highlighting the usage of `infer` to retrieve a part of a longer string literal type.

---

The [properties.ts](./properties.ts) file contains an interface which has properties with long key names (like `Octopus.Action.Kubernetes.WaitForJobs`). Those key names contain a common prefix, so ideally we should be composing the long key name from short names, which would make it easier for the user to access the property values.

However, that file may not be editable (maybe in another package, or generated). Is there still a way to utilize the common prefix to save some typing (_pun intended_)? To do this, we need the `infer` keyword, which in this context can be seen as the inversion of string literal conncatanation type. The implementation is in [index.ts](./index.ts).

---
[Home](../../../../../README.md)