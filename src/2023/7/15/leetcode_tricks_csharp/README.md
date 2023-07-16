# Twelve C# Features You Should Know to Write More Elegant LeetCode Solutions

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

Tuple is one of the most useful language features when it comes to speedy one-off coding like in LeetCode, because you can associate many fields together without having to create a separate type for it.

For example, sometimes you want to maintain a stack of elements, but every time you push some element to the stack, you also need to record its index in the original array. Instead of using two parallel stacks to store the element and index separately, you can simply use a tuple:

```csharp
var stack = new Stack<(int, int)>();

// Push the element and index together to the stack
stack.Push((3, 5));

// Pop the element and index from the top of the stack with tuple unpacking. Note that you can also peek the top of the stack without having to remove the elements by using .Peek()
var (element, index) = stack.Pop();
```

You can also name the tuple fields. Doing this will make the code easier to read when both the index and the element are of type `int`, for example. The above code can also be written as:

```csharp
var stack = new Stack<(Element: int, Index: int)>();

// Push a tuple with field names
stack.Push((Element: 1, Index: 2));

// But you can also use it without field names
stack.Push((2, 3));

// Danger! This does not swap Index and Element automatically. It will assign Element to 2 and Index to 3
stack.Push((Index: 2, Element: 3));
```

Note that field names are informational only. They are not enforced. Ultimately it is the order of the fields that decides where each field will be assigned. If you do want some extra safety, consider using a record:

```csharp
record Entry(int Element, int Index);

var stack = new Stack<Entry>();
stack.Push(new Entry(Element: 1, Index: 2));
stack.Push(new Entry(2, 3));

// with record, the fields are matched by name, so this is correct
stack.Push(new Entry(Index: 2, Element: 3));
```

However, as you can see, there is a bit more to type to use records.

Both records and tuples have the default comparator implemented to take into consideration of the fields in the order of declaration, so you can directly sort a list of tuples:

```csharp
var intervals = new List<(int Begin, int End)>
{
    (2, 3), (1, 2), (1, 3), (3, 1), (2, 2)
};

intervals.Sort();
// Sorted first by Begin, then by End:
// (1, 2), (1, 3), (2, 2), (2, 3), (3, 1)

```

Tuples can also be used as the return value of methods:

```csharp
public int Fib(int n) => Fib2(n).Item1;

(int, int) Fib2(int n)
{
    if (n == 0)
    {
        return (0, 1);
    }
    var (a, b) = Fib2(n - 1);
    return (b, a + b);
}
```

The above code computes the nth finocacci number using recursion, but because the inner method returns 2 numbers at the same time, the time complexity is O(n). If we used a single return value, the time complexity will be exponential. See [509. Fibonacci Number](https://leetcode.com/problems/fibonacci-number/).

Finally, in case you don't know yet, tuples are handy for swap variables without needing to create a temporary variable:

```csharp
var a = 1;
var b = 2;
(a, b) = (b, a); // now a == 2, b == 1
```

## 4. Nested mothods

Sometimes you need a private method that takes a few more arguments, and the public method just delegates the computation to this private method with some initial values. If the private method requires some common arguments, such as the memo dictionary for dynamic programming, you should consider using a nested inner method, so you don't have to pass some variable each time:

```csharp
public int MinCostClimbingStairs(int[] cost) 
{
    var minCosts = new Dictionary<int, int>();
    int MinCosts(int[] cost, int n)
    {
        if (n < 0)
        {
            return 0;
        }

        if (minCosts.ContainsKey(n))
        {
            return minCosts[n];
        }

        var result = Math.Min(MinCosts(cost, n - 1), MinCosts(cost, n - 2));
        result += n < cost.Length ? cost[n] : 0;

        minCosts.Add(n, result);

        return result;
    }

    return MinCosts(cost, cost.Length);
    }
```

The above is a top-down dynamic programming implementation of [746. Min Cost Climbing Stairs
](https://leetcode.com/problems/min-cost-climbing-stairs). The `minCosts` variable is a memoization cache to avoid exponential time complexity. If we didn't declare the private `MinCosts` as a nested method, we'll have to pass this as a separate argument.

## 5. LINQ

Needless to say, LINQ is one of the most loved features in C#. These LINQ methods are handy for LeetCoding:

- ### `Select`
  Project one sequence to another:
  ```csharp
  // Cast the input int array to long
  var ns = inputs.Select(n => (long)n);
  ```

- ### `Where`
  Filtering:
  ```csharp
  var divisibleBy3 = inputs.Where(n => n % 3 == 0);
  ```

- ### `Aggregate`
  Accumulate elements:
  ```csharp
  // intevals is an array of array representing intervals.
  var intervals = new int[][]
  {
      new[] { 1, 2 },
      new[] { 2, 3 },
      new[] { 1, 3 },
      new[] { 4, 6 }
  };

  var totalLength = intervals.Aggregate(0, (acc, cur) => acc + cur[1] - cur[0]);
  ```

  Most of times though, using `Sum` is more convenient, see below.

- ### `Min`, `MinBy`, `Max`, `MaxBy`, `Sum`
  Handy for arithmetic:
  ```csharp
  var min = inputs.Min();
  var max = inputs.Max();
  var sum = inputs.Sum();
  
  int Len(int[] interval) => interval[1] - interval[0];
  var shortest = intervals.MinBy(Len);
  var longest = intervals.MaxBy(Len);
  var totalLength = intervals.Sum(Len);
  ```

- ### `OrderBy`, `ThenBy`, `GroupBy`
  ```csharp
  // sort by start point, then by end point
  var sorted = intervals.SortBy(interval => interval[0])
    .ThenBy(interval => interval[1]);

  // for each start point, pick the shortest one
  var shortestForEachStartPoint = intervals.GroupBy(interval => interval[0])
    .Select(group => group.OrderBy(interval => interval[1]).First());
  ```

- ### `Zip`
  Handy for associating two arrays:
  ```csharp
  // Accociate two input arrays, nums1 and nums2 together,
  // and then sort descending according to elements in nums2
  var elements = nums1.Zip(nums2)
    .OrderBy(pair => -pair.Item2)
    .ToList();
  ```

Note that using LINQ does have some performance panalty. For example, when the input is an array rather than a List, you should probably directly sort the array in-place. See below.

## 6. Array.Sort

Because often the inputs of LeetCode problems are arrays rather than Lists, using `Array.Sort` is often more efficient than doing `OrderBy` and `ThenBy` because it does the sorting in-place. One thing to note is that the `Array.Sort` methods can take a lambda function as the Comparison:

```csharp
var arr = new int[] { 3, 4, 5, 1, 2 };

// sort ascending:
Array.Sort(arr);

// sort descending:
Array.Sort(arr, (a, b) => b - a);
```

## 7. Array.BinarySearch

Using Comparator


## 8. Stack, Queue, List, LinkedList

Stack and Queue for DFS and BFS

Fixed-size Stack is equivalent to using an array



## 9. PriorityQueue, SortedSet

Heap

## 10. Generators

Generators are handy if you want to abstract some kind of iteration as a normal sequence. For example, you can write a generator method to do the BFS iteration of a binary tree, and becauese the result will be an IEnumerable, you can use LINQ to query the results just like normal IEnumerables. See [199. Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view):

```csharp
public IList<int> RightSideView(TreeNode root) => Bfs(root)
    .GroupBy(node => node.Level)
    .Select(group => group.First().Node.val)
    .ToList();

IEnumerable<(TreeNode Node, int Level)> Bfs(TreeNode root)
{
    var queue = new Queue<(TreeNode Node, int Level)>();

    queue.Enqueue((root, 0));
    while (queue.Count > 0)
    {
        var (cur, level) = queue.Dequeue();
        if (cur is null)
        {
            continue;
        }
        
        yield return (cur, level);

        queue.Enqueue((cur.right, level + 1));
        queue.Enqueue((cur.left, level + 1));
    }
}
```

The above code use a private method `Bfs` to do a breath-first iteration of the binary tree and includes the level index of the node. Then we can simply find the right-most elements for each level with LINQ.

Generators are also useful if you want to create an infinite sequence. For example, the following `Primes` method will generate prime numbers indefinitely:

```csharp
IEnumerable<int> Primes()
{
    var primes = new List<int>();
    var i = 1;
    while (true)
    {
        i++;
        if (!primes.Any(p => i % p == 0))
        {
            primes.Add(i);
            yield return i;
        }
    }
}
```

Then, you can use the `Take` LINQ method to get the first `n` prime numbers:

```csharp
public IList<int> Primes(int n) => Primes().Take(n).ToList();
```

## 11. `BigInteger`

You perhaps don't see this very often in your day-to-day work, but in LeetCode, quite a lot of integer related question will include some test cases that have extremely large inputs that will overflow the `int` type which represents a 32-bit integer.

To make it even trickier, some questions claim that the result is guaranteed to fit into a 32-bit integer, but if you trust it, you get wrong answers, too! Because although the final result can fit into a 32-bit integer, the intermediate results can overflow as well.

Most of times you can solve this by using `long` type instead in the computation process, which has 64 bits. But there are occasions when the `long` type isn't big enough. For example, the inputs may already be in the `long` type, or the problem states you need integers of arbitrary length.

In these scenarios, the `BigInteger` type comes in handy. It is pretty much a drop-in replacement for `int`, because it has overridden all the arithmetic operators, and it also supports implicit conversion from a normal `int`. So, apart from declaring your variable as `BigInteger` and remembering to cast the final result back to `int`, there is really not much else to do.

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