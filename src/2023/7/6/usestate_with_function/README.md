# A Pitfall when Using `useState` for Loading a Function

Normally the `useState` hook in React can be used with the `useEffect` hook to initialize a state when a component load (that is, lazy loading). However, when the state to be loaded is a function, there is a pitfall.

A common lazy loading pattern is like:

```ts
const [myState, setMyState] = useState("")

useEffect(() => {
    async function loadState() {
        const state = await someFunctionThatRetrievesDataAsync("https://data")
        setMyState(state)
    }
    loadState()
}, [])
```

The `myState` state variable will be loaded when the component first loads.

What if the state to be loaded is a function? Will anyone ever need to do this?

It turned out, yes, sometimes the function is loaded from a remote location, for example, WebAssembly!

```ts
// Note: this version doesn't work

const [myFunc, setMyFunc] = useState(null)

useEffect(() => {
    async function loadFunc() {
        // load the function from a webassembly wrapper
        const { func } = await import("../public/assets/func")
        setMyFunc(func)
    }
    loadFunc()
})

// invoking the function later
if (myFunc) {
    await myFunc()
}

```

The intention here is to load the `myFunc` when the component first loads, and use it later. There is a subtle bug, did you notice it?

Ok, let me reveal the answer here. The bug is, apart from directly taking the new value, the `setMyFunc` function can also take a function which updates the original `myFunc` value to a new value. 

In other words, if the argument given to `setMyFunc` is a function (which it always is), it will be invoked first, and then its return value is set to the `myFunc` variable. Because the new value itself _is_ a function, it is immediately invoked directly. This is not desired because this isn't the correct time we want to invoke the `myFunc` function, and it won't be invoked with the correct arguments.

The fix is simple:
```diff
-         setMyFunc(func)
+         setMyFunc(() => func)
```

To sum up, when using `const [state, setState] = useState(...)`, `setState` can either take directly the new value, or a function that returns the new value. It is very intuitive when working with normal values. But when the `state` itself is a function, it is a pitfall because you have to wrap it inside a thunk to prevent the resolved function from being called immediately.


> Note: I met this problem when building the [Octostache Playground](https://github.com/y1hao/octostache-playground).

---
[Home](../../../../../README.md)