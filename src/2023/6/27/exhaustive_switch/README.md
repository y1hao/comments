# Write an Exhaustive `switch` Statement in TypeScript

How to do an exhaustive `switch` in TypeScript.

TypeScript's type checker is very powerful. In the case of a `switch` statement, it can infer what possible types for a logic branch can be. With this we can make an exhaustive checker, so that the switch statement must cover all possible cases to pass the type check.

The implementation is straightforward: use the `never` type.

```typescript
function exhaustiveCheck(_: never) {}

type T = "a" | "b" | "c"

function doSwitch(t: T) {
    switch (t) {
        case "a": break
        case "b": break
        case "c": break
        // if any of the above cases is missing, 
        // or new elements are added to type T,
        // the type check will fail
        default: exhaustiveCheck(t)
    }
}
```

---
[Home](../../../../../README.md)