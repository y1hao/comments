# Patching a Built-in Type in Python

Demostrates how to monkey-patch a built-in type.

In Python you can make modifications to built-in types by `import builtins`. However, the modification does not apply to literals. For example:

```python
import builtins

class MyStr(str):
    def print(self):
        return print(self)

builtins.str = MyStr

str("Hello").print() # Output: Hello - builtin type patched!
"Hello".print()      # raises AttributeError: 'str' object has no attribute 'print' - not working for literals
```

It will look more consistent and be easier to read and write, if we can make this work for literals as well. In fact, we can do this, but it just requires some tricks. See this code:

```python
import gc

gc.get_referents(str.__dict__)[0]["print"] = lambda self: print(self)

"It works!".print() # Output: It works!

```

The magic here is to use the `gc.get_referents()` method, which gets the referenced objects. `str.__dict__` is a `mappingproxy` which represents a readonly view of the underlying dict which holds all the members of `str`. By the `gc` trick we get the underlying mutable instance, and then we are free to modify it.

> I didn't say this is good practice!

The following code is a more comprehensive example which illustrates how to hack the built-in string type to make it behave like a context manager. After the magic, we can use the a string literal with the keyword `with`:

```python
import gc

def enter(self):
    print(self)

def exit(self, type, value, traceback):
    if type == None:
        print("PASSED!")
    else:
        print("FAILED!")

gc.get_referents(str.__dict__)[0]["__enter__"] = enter
gc.get_referents(str.__dict__)[0]["__exit__"] = exit

with "Test 1 should be 1":
    assert 1 == 1

# Output:
#   Test 1 should be 1
#   PASSED!

with "Test 1 should be 1":
    assert 1 == 2

# Output:
#   Test 1 should be 1
#   FAILED!
#   Traceback (most recent call last):
#     File "<stdin>", line 2, in <module>
#   AssertionError
```

The code adds the `__enter__` and `__exit__` methods to the builtin `str` type, making it a context manager. We print the string in the `__enter__` method, and then we run the code inside the `with` block. If there are any exceptions raised, we print `FAILED!` from `__exit__`, otherwise we print `PASSED!`. In essence, we've hacked the str type into a testing framework!

> I learned this `gc` trick from the [forbiddenfruit](https://github.com/clarete/forbiddenfruit) library.

---
[Home](../../../../../README.md)