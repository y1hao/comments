import { Properties } from "./properties";

// an example value
const props: Properties = {
    "Octopus.Action.Kubernetes.ExecutionTimeout": 180,
    "Octopus.Action.Kubernetes.WaitForJobs": true,
    "Octopus.Action.Kubernetes.DeploymentStyle": "BlueGreen"
}

// The name is quite long. A lot of typing to do to get the value
const timeout = props["Octopus.Action.Kubernetes.ExecutionTimeout"];

// Create a helper function to create full name from the last part of the name,
// while remaining strongly typed

// The prefix
type Prefix = "Octopus.Action.Kubernetes.";
// Mapping from a string as the short name, to a full name
type FullNameOf<T extends string> = `${Prefix}${T}`;
// The inversion of FullNameOf. Note the use of infer
type ShortNameOf<T> = T extends FullNameOf<infer ShortName> ? ShortName : never;
// All valid full names
type FullName = keyof Properties;
// All valid short names. First create a fullname: shortname mapping, then select the values
type ShortName = { [Name in FullName]: ShortNameOf<FullName> }[FullName]

// Finally, we can properly type this helper function
function fn(shortName: ShortName): FullName {
    return `${"Octopus.Action.Kubernetes."}${shortName}`;
}

// Now, we make it easier to get the property values
const t = props[fn("ExecutionTimeout")];