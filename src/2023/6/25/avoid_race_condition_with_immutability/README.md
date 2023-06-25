# Avoid Race Conditions and Invalid States with Immutability

How designing with immutability helps avoid race conditions and invalid states in C# concurrent programming.

## Context

We need to write a poller that polls the statuses of a list of items periodically. The requirements are:
- Once started, the poller will poll against the statuses of a list of items once every 2 seconds.
- While the poller is running, some more items may be discovered, so the poller should be able to accept more items. After more items are added, subsequent polls should include those new items.
- When no more items need to be added, the caller of the poller can signify this. Then, the poller will continue to run for 10 seconds before it completes.

## PollerV1

The [PollerV1](./PollerV1.cs) class is a straightforward but somewhat naive implementation. The interface is like this:

```csharp
public interface IPollerV1
{
    void Start();
    void AddMore(params string[] items);
    Task WaitAndComplete();
}
```

The caller of this class will start the poller by calling `Start` first, and internally the poller starts a task on a separate thread by calling `Task.Run` which performs the polling. The caller can call `AddMore` to add more items. When no more items are needed, the caller calls `WaitAndComplete`, which polls for another 10 seconds and returns.

To running the example program with PollerV1, run:
```sh
dotnet run v1
```

Although the idea is straightforward, the implementation is tricky to get right. 

One concern is thread safety. The thread which performs the polling, and the thread which calls the poller, both access the list of items, as well as the private variable `_hasMore`. To avoid race condition, we need locks or other synchonization mechanisms (in [PollerV1](./PollerV1.cs) we used locks). This adds much complexity, and can potentially lead to dead locks.

Another concern is that this implementation requires the caller of the poller class to call methods in the correct order. If the the method `WaitAndComplete` is called before `Start`, for example, because the private `_task` has not been created yet, this will throw a null reference exception.

How can we improve the implementation, so that we
- avoid race condition while not having to use locks, and
- make sure the methods are always called in the correct order by the caller?

## PollerV2

The idea is, we make the poller immutable. Everytime we want to make modifications to the poller, instead we cancel the current running poller and create a new one. In addition, we represent different states of the poller by using distinct types. Each only contains the valid operations it can do. The interfaces look like:

```csharp
public interface IPollerV2
{
    IWaitForMorePoller Start();
}

public interface IWaitForMorePoller
{
    Task<IWaitForMorePoller> WithMore(params string[] items);
    Task<IWaitForTimeoutPoller> WithTimeout();
}

public interface IWaitForTimeoutPoller
{
    Task WaitAndComplete();
}
```

There are more interfaces now, but each of them only contain valid operations. The caller starts by creating an instance of `IPollerV2`, which only contains a single method `Start`. By calling this method, instead of modifying the poller instance, a new poller of type `IWaitForMorePoller` is returned. The caller can add more items by calling `WithMore` or complete adding items and wait for the 10 seconds timeout by calling `WithTimeout`. All methods do not modify the current poller instance (apart from stopping the polling). They always create new instances which contains the updated polling task.

This way, we make invalid states unrepresentable, because all methods on the types are valid. We can also get rid of locks, because now we do not share variables between threads, instead we cancel the task in the previous thread before we run the new task in a thread.

The full implementation is in [PollerV2.cs](./PollerV2.cs).

Run it with:
```sh
dotnet run v2
```

## Conclusion

This example demostrates that designing with immutability can help us avoid the usages of locks or getting into invalid states. Concurrent programming is tricky. But with careful thinking and design, the problem is often not as concurrent as we thought.

---
[Home](../../../../../README.md)