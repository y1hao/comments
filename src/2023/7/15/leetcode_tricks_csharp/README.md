# 12 C# Features You Should Know for Writing LeetCode Solutions More Elegantly

> 12 tricks I learned from solving 200+ LeetCode problems in C#, which can help you write solutions in a more elegant and idiomatic way.

Well, C# isn't the most popular language of choice when it comes to LeetCoding. You can find solutions in Python and/or Java to almost all problems, but only occasionally can you see solutions in C#. Even when there is a C# solution, often it just looks like a direct translation from Java. But in fact, C# is an expressive language and is continuously evolving. There are quite some nice language features that can help you write LeetCode solutions in a faster and more elegant way.

Here I'd like to share with you the 12 tricks I learned from solving 200+ LeetCode problems in C#.

## 1. 2D arrays

Let's start with an easy trick. In many languages there are only one-dimensional arrays. When you need to represent something like a matrix, you need to create an "array of arrays" (or [jagged array](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/arrays/jagged-arrays), in C#'s terminology).

This is not a big problem, but in LeetCode settings it's not very convenient, because you have to remember to initialize each row separately. For example, to create a 10 * 10 matrix, with jagged array, you'll need to write:

```csharp
var matrix = new int[10][];
for (var i = 0; i < matrix.Length; i++)
{
    matrix[i] = new int[10];
}
```

Not only is this a lot to type, it is also tricky to get the syntax right (which pair of square brackets should I write the size in?)

More importantly, you'll get an exception if you forget to do the for-loop:

```js
var matrix = new int[10][10];
matrix[0][0] = 5; // NullReferenceException!
```

In C#, a better way is to use truely [multi-dimensional](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/arrays/multidimensional-arrays) arrays, which allows you to skip the row-by-row initialization code:

```csharp
var matrix = new int[10, 10];
matrix[0, 0] = 5; // No exceptions!
```

Using a 2D array can save you a bit of typing, and prevent mistakes from not initializing rows. Note that for 2D arrays, all rows must be of equal length, and every "cell" will be initialized with the default value (`0` for integers, `false` for `bool`, and `null` for objects including `string`s).

## 2. Negative Indices and Ranges

Since C# 8.0, you can use `^` to indicate that an index counts from the end. In many scenarios you want to get the last element in an array, a list, or a string. Instead of writing:

```csharp
var last = arr[arr.Length - 1];
```

You can simply write:

```csharp
var last = arr[^1];
```

Also, you can use `..` to create a substring or subarray (ie. a [Range](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/proposals/csharp-8.0/ranges)). For example, the following code tests if a string can be constructed by repeating a shorter string multiple times (see [459. Repeated Substring Pattern](https://leetcode.com/problems/repeated-substring-pattern)).

```csharp
public bool RepeatedSubstringPattern(string s) 
    {
        for (var i = 1; i <= s.Length / 2; i++)
        {
            if (s[i..^0] + s[0..i] == s)
            {
                return true;
            }
        }
        return false;
    }
```

Here, `s[i..^0]` is the right part of string `s` beginning from the `i`th character (inclusive). `s[0..i]` is the left part of string `s` ending before the `i`th character (exclusive). 

The ranges are always half open, including the beginning element and excluding the ending element. `^1` matches the last element, and `^0` represents the non-existing "element" after the last, so that `x..^0` can include the last element as well.

Note that ranges have a drawback: they create a new instance for the subarray or substring. This might not be desirable for LeetCode problems. Most times you should just use the same array and record the beginning and ending indices. But the `arr[^1]` trick can be quite useful in many situations.

## 3. Tuples


## 4. Nested mothods


## 5. LINQ


## 6. Array.Sort


## 7. Array.BinarySearch


## 8. Stack, Queue, List, LinkedList


## 9. PriorityQueue, SortedSet


## 10. Generators


## 11. `BigInteger`

You perhaps don't see this very often in your day-to-day work, but in LeetCode, quite a lot of integer related question will include some test cases that have extremely large inputs that will overflow the `int` type which represents a 32-bit integer.

To make it even trickier, some questions claim that the result is guaranteed to fit into a 32-bit integer, but if you trust it, you get wrong answers, too! Because although the final result can fit into a 32-bit integer, the intermediate results can overflow as well.

Most of times you can solve this by using `long` type instead in the computation process, which has 64 bits. But there are occasions when the `long` type isn't big enough. For example, the inputs may already be in the `long` type, or the problem states you need integers of arbitrary length.

In these scenarios, the `BigInteger` type comes in handy. It is pretty much a drop-in replacement for `int`, because it has overridden all the arithmetic operators, and it also supports implicit conversion from a normal `int`. So, apart from declaring your variable as `BigInteger` and remembering to cast the final result back to `int`, there is really not much to do.

For example, the following `Factorial` method computes the factorial of a non-negative integer `n`, and returns the result as modulo of (10^9 + 7) since it can be very large (this is a common requirement in LeetCode questions).

```csharp
public int Factorial(int n)
{
    if (n <= 1)
    {
        return 1;
    }
    BigInteger result = 1;
    for (var i = 2; i <= n; i++)
    {
        result *= i;
    }
    return (int)(result % 1_000_000_007);
}
```

## 12. `BitOperations`

Some questions require bit manipulations. The `BitOperations` class comes in handy. It defines static methods such as:

- `PopCount`
- `LeadingZeroCount`
- `TailingZeroCount`
- `RotateLeft`
- `RotateRight`

The `PopCount` method is perhaps the most useful. It counts the numebr of `1`s in the integer's bit representation.

For example, given integers `a`, `b` and `c`, the following `MinFlip` method returns the number of flips required in numbers `a` and `b` to make `a | b` equal to `c`. A flip means changing a `1` bit to `0` or vice versa. (See [1318. Minimum Flips to Make a OR b Equal to c](https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/))

```csharp
public int MinFlips(int a, int b, int c) =>
    BitOperations.PopCount((uint)((a | b) ^ c)) 
         + BitOperations.PopCount((uint)(a & b & ((a | b) ^ c)));
```

---

To wrap up, these C# features make it a wonderful language to use for LeetCoding. Getting yourself familiar with them speeds up your problem solving, and helps you write more elegant and expressive C# code.

Happy coding!

---
[Home](../../../../../README.md)