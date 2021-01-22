### Functional Python

This series of articles shows a natural example of using higher-order functions in Python. We won't stop at building a parametrized decorator, as most of the examples on the web do. Instead, we will move on step by step away from procedural and object programming. Exploring common problems of development, we will solve them using features of functional programming in Python.

# Part 1. Higher-Order Functions: Method as a Decorator

Let's start small and not so far away from OOP. Most of the beginners in programming are taught Object-Oriented Programming right at the start of their education. Hence, we will start from something that is quite commonly.

## The Task

Let's imagine, we join a new project with much of a "framework" code to write. Our first task, we are expected to have the cache API as an object with some easy to use methods. Of course, there are many awesome caching libraries at the [PyPI](https://pypi.org/search/?q=caching) but, hey, the situation is all set-up for us to learn while writing code.

> NB: In real developer practice, always look for an opportunity to evaluate existing solutions first, before deciding to write your own. [*Not Invented Here*](https://en.wikipedia.org/wiki/Not_invented_here) sickness might be a serious condition for a programmer.

Here is a scaffold that the codebase already has:

```python
class Cache:
    """
    This class should know how to cache things.
    """
    _engine: CacheEngine

    def build_key(self, params: CallParams) -> Key:
        """
        This method knows how to create a key (some kind of `str`) from
        any call parameters.
        """
```

We would want to use awesome [decorator syntax](https://book.pythontips.com/en/latest/decorators.html) of Python and be able to write something like this to enable caching for the function.

```python
@decorator
def foo(*some_args, **some_kwargs): ...
```

## The Context

Imagine there's a function that we consider expensive, with some kind of computations, networking, or other optimization involved. We need to remember its outcomes for some time, aka. cache it. The value might become obsolete at some point of the time, which will require executing the function again.

```python
def expensive_function(*some_args, **some_kwargs): ...
```

Let's assume there is a class named `CacheEngine`, which knows how to save and read things. It might be a kind of in-thread memory store, an integration with Redis or Memcached, or some sort of persistence. Its details are irrelevant at the moment. Much about it can change, so we want to enclose this area of change into a separate class.

```python
class CacheEngine:

    def load(key: Key) -> Value: ...

    def store(key: Key, value: Any) -> None: ...
```

Let's state some definitions that will help write meaningful [*annotations*](https://realpython.com/python-type-checking/#type-systems) as function [*signatures*](https://en.wikipedia.org/wiki/Type_signature#Method_signature).

```python
# A type for keys of the cache
Key = typing.NewType("Key", str)
# A type variable for the values returned by the function
# Let's keep things as generic as we can
Value = typing.TypeVar("Value")
# An abbreviation for cachable function.
# This is our 1st order of abstraction.
Function = typing.Callable[..., Value]
# A sentinel object representing value not yet set in the cache
# > NB: Recall that None can be a valid result of a function, so don't use
#   the None as a default value in cache mechanics.
NotSet = unittest.mock.sentinel.NotSet

# An abstraction for params of a function call
@dataclasses.dataclass(frozen=True)
class CallParams:
    args: t.Tuple
    kwargs: t.Dict[str, t.Any]
```

## 1. Requirement: Caching Decorator

Let's get down to the task. Using previous definitions, we'll write a method that will work as a caching decorator.

```python
class Cache:
    ...

    def cache_function_decorator(self, f: Function) -> Function:
        @functools.wraps(f)  # (1)
        def wrapper(*args, **kwargs) -> Value:  # (2)
            key = self.build_key(Call(args, kwargs))
            if value_from_cache := self._engine.load(key) is not NotSet:  # (3)
                return value_from_cache
            value = f(*args, **kwargs)  # (4)
            self._engine.store(key, value)
            return value

        return wrapper  # (5)
```

So... let's use this new method.

> NB: here we annotate different fragments of code with "*time*" of their execution: *configuration*-time, *import*-time and *usage*-time. For now, it has no meaning for us, but later on we'll see some problems that might take place here.

```python
# configuration-time
cache = Cache()

# import-time
@cache.cached  # (6)
def expensive_function(some_context, *args, **kwargs):
    """My docstring."""

# usage-time
expensive_function("foo")  # now I'm running the computations...
expensive_function("foo")  # ... and now I'm not
expensive_function("bar")  # ... and now again I'm running my computations because arguments differ
assert expensive_function.__name__ == "expensive_function"  # (7)
assert expensive_function.__doc__ == "My docstring."  # (7)
```

Now, after using the decorator method `(6)`, your `expensive_function` variable holds the reference to the `wrapper` function `(2)`. Why? At the `(5)`, the `cache_function_decorator` has returned a new function that uses the original function to  call it `(4)` under some conditions `(3)`. That's why we can call `cache_function_decorator` as a 2nd Order Function. This is a *signature* of the decorator:

```python
(self: Cache, f: Function) -> Function
```

In this perspective, a decorator is just a function that takes a function as its main argument and the `@` syntax is just a [*syntactic sugar*](https://en.wikipedia.org/wiki/Syntactic_sugar). The exact effect would happen using the following notation instead of `(6)`.

```python
expensive_function = cache.cached(expensive_function)
```

But how this all works? Why `f` and `self` are defined in the scope of the `wrapper` `(4)`? Well, `wrapper` is called a [*closure*](https://en.wikipedia.org/wiki/Closure_(computer_programming)) with respect to `cache_function_decorator`, because it uses names from the scope of the function in which it was declared for. Python interpreter implicitly passes all names with their runtime values from the `cache_function_decorator` to the `wrapper`. We'll see much more use of this mechanism further on.

There is one more thing worth noticing. Although `cache_function_decorator` returns a new function, created inside of it `(5)`, this function identifies exactly the same as the original one `(7)`. This is the case because of the helper `functools.wraps` decorator `(1)`. It copies metadata of a function onto another one (its decorator, in this case). For now, this quite common feature is purely cosmetic, but later we'll see it important to the mechanics of our caching.

> NB: `functools.wraps` is a visible example from the standard library of Python where a decorator is used to enrich a function or modify its behavior in a functional programming way.
