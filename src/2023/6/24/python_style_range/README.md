# Make a Python-Style `range` in C# with Tuples and Duck Typing

How to take advantage of duck-typing in C# to turn a Tuple into a Python-style `range` which can be iterated over by `foreach`.

I like Python's `range` function:
```python
# prints 1 and 2
for i in range(1, 3):
    print(i)
```

You can also define the step:
```python
# prints 1 and 3
for i in range(1, 4, 2):
    print(i)
```

In C#, we also have `Enumerable.Range`. But it is not as handy as `range` in Python sometimes:
- It is very long to type!
- It takes the start and the _count_ as arguments, not the start and the exclusive end, which can be confusing sometimes.
- It doesn't take the step as the third argument.

Can we make something slightly better? Yes. With a bit of magic utilising the Tuple type and duck typing, we can get something like this:

```csharp
using RangeExtensions;

// prints 1 and 2
foreach (var i in (1, 3))
{
    Console.WriteLine(i);
}

// prints 1 and 3
foreach (var i in (1, 4, Step: 2))
{
    Console.WriteLine(i);
}
```

We are re-using the Tuple literals as ranges, as long as you import `RangeExtensions`.

Note the `Step` parameter can be named, too. This makes it a bit clearer than the Python `range` which you can name the parameters.

The implementation is in [Range.cs](./Yihao.Range/Range.cs).

---
[Home](../../../../../README.md)