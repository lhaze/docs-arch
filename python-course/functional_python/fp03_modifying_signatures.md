### Functional Python by Examples

This series of articles shows plain examples of using functional programming in Python. We won't stop at building a parametrized decorator, as most of the examples on the web do. Instead, we will move on step by step away from procedural and object programming. Exploring common problems of development, we will solve them using features of functional syntax in Python.

- [Part 3. Higher-Order Functions: Modifying Signatures](#part-3-higher-order-functions-modifying-signatures)
  - [The Context](#the-context)
  - [Requirement: Decorating a Method](#requirement-decorating-a-method)
  - [Requirement: Injecting an Attribute](#requirement-injecting-an-attribute)
  - [Conclusions](#conclusions)

[⇦ Previous: Higher-Order Functions: Method as a Decorator Factory](fp02_method_as_decorator_factory.md)

[Next: Higher-Order Functions: Composing Decorators ⇨](fp04_composing_decorators.md)

# Part 3. Higher-Order Functions: Modifying Signatures

## The Context

Last time we left our code having a class which provides caching abilities. Its main method is a parametrized decorator.

```python
class Cache:
    ...

    def cache_function_decorator(
        self, f: Optional[Function] = None, *, expire: int = None
    ) -> Callable[[Function], Function]:
        def cached_function(f: Function) -> Function:
            @functools.wraps(f)
            def wrapper(*args, **kwargs) -> Value:
                key = self.build_key(CallArgs(args, kwargs))  # (1)
                if value_from_cache := self._engine.load(key) is not NotSet:
                    return value_from_cache
                value = f(*args, **kwargs)
                self._engine.store(key, value, expire=expire)
                return value

            return wrapper

        if f is None:
            return cached_function
        else:
            return cached_function(f)
```

Our sample usage of the cache can be presented with the following snippet:

```python
cache = Cache()

@cache.cache_function_decorator(expire=7)
def expensive_function(*some_args, **some_kwargs):
    ...
```

## Requirement: Decorating a Method

The next day, the yet known fellow team member, Dave, shows up to warn us, that our caching feature doesn't work. They're using the decorator and nothing happens -- all calls are executed. Let's look at how Dave is doing it:

```python
cache = Cache()

class Service:

    @cache.cache_function_decorator(expire=7)
    def expensive_method(self, *some_args, **some_kwargs):  # (3)
        ...

def process(cls):
    instance = Service()  # (3)
    instance = expensive_function(*some_args)
```

Oh, bugger! You haven't known, they are going to decorate a method of a short-lifespaned object.
Instances of `Service` are created only for a while `(3)`, and yet they participate in creating the set of arguments of the call `(2)`. This means each time the `expensive_method` is called, cache is differentiating the call with `self` argument. Not good. It seems you should provide a way for the cache to chop off some arguments of the call while regarding building the key for the call `(1)`. You probably want to chop of `self` argument, but there may be more arguments that are [*volatile*](https://en.wikipedia.org/wiki/Volatile_(computer_programming)) and aren't supposed to be regarded to the cache key.

> NB: Quite common example of a *volatile* value is a `request` instance to a web server application. You probably don't want to cache things only for the current request.

Ok, let's generalize the problem a bit. We are looking for a class of functions that transform a `CallArgs` into another `CallArgs`:

```python
(CallArgs) -> CallArgs

# for example:

def transform_call_args(call: CallArgs) -> CallArgs:
    args = call.args[1:]  # (4)
    kwargs = call.kwargs.pop('request', None)  # (5)
    return CallArgs(args, kwargs)
```

or

```python
(*args, **kwargs) -> CallArgs

# for example

lambda self, request, *args, **kwargs: CallArgs(args, kwargs)  # (6)
```

## Requirement: Injecting an Attribute

(...)

## Conclusions

(...)

If you want to see how this works in practice, take a look at our [working and tested example](fp03_modifying_signatures.py).

[Next: Higher-Order Functions: Composing Decorators ⇨](fp04_composing_decorators.md)
