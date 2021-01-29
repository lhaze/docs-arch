### Functional Python by Examples

This series of articles shows plain examples of using functional programming in Python. We won't stop at building a parametrized decorator, as most of the examples on the web do. Instead, we will move on step by step away from procedural and object programming. Exploring common problems of development, we will solve them using features of functional syntax in Python.

- [Part 2. Higher-Order Functions: Method as a Decorator Factory](#part-2-higher-order-functions-method-as-a-decorator-factory)
  - [The Context](#the-context)
  - [The Task](#the-task)
  - [Requirement: Passing Parameters to the Decorator](#requirement-passing-parameters-to-the-decorator)
  - [Requirement: Backward Compatibility](#requirement-backward-compatibility)
  - [Conclusions](#conclusions)

[⇦ Previous: Higher-Order Functions: Method as a Decorator](fp01_method_as_decorator.md)

[Next: Higher-Order Functions: Modifying Signatures ⇨](fp03_modifying_signatures.md)

# Part 2. Higher-Order Functions: Method as a Decorator Factory

## The Context

We will pick up where we left off last time. We have a class that successfully caches function calls in a very simple way. Though, the cache stays remembered as long as the engine keeps it.

```python
class Cache:

    _engine: CacheEngine

    def build_key(self, call: CallArgs) -> Key:
        ...

    def cache_function_decorator(self, f: Function) -> Function:
        @functools.wraps(f)
        def wrapper(*args, **kwargs) -> Value:
            key = self.build_key(CallArgs(args, kwargs))
            if value_from_cache := self._engine.load(key) is not NotSet:
                return value_from_cache
            value = f(*args, **kwargs)
            self._engine.store(key, value)
            return value

        return wrapper
```

## The Task

Now, we are tasked to enhance our decorator so that we can explicitly tune the expiration time (aka. [*time to live*, TTL](https://en.wikipedia.org/wiki/Time_to_live)) per cached function. The easiest way to do this is to make your method (the one that was the decorator in the last episode) accept parameters as arguments.

## Requirement: Passing Parameters to the Decorator

```python
class Cache:
    ...

    def cache_function_decorator(
        self, expire: int = None  # (1)
    ) -> Callable[[Function], Function]:  # (2)
        def cached_function(f: Function) -> Function:
            @functools.wraps(f)
            def wrapper(*args, **kwargs) -> Value:
                key = self.build_key(CallArgs(args, kwargs))
                if value_from_cache := self._engine.load(key) is not NotSet:
                    return value_from_cache
                value = f(*args, **kwargs)
                self._engine.store(key, value, expire=expire)
                return value

            return wrapper
```

That wasn't so hard, right? The same technique of building a function as a closure but taken one step higher. The new `cache_function_decorator` has the following signature:

```python
(self: Cache, expire: int) -> Callable[[Function], Function]
```

and should be used in this way:

```python
# import-time
@cache.cache_function_decorator(expire=7)  # (3)
def expensive_function(*some_args, **some_kwargs): ...

@cache.cache_function_decorator()  # (4)
def another_expensive_function(*some_args, **some_kwargs): ...
```

Now, the method takes arguments `(3)` and returns the actual decorator. Wait a minute! It's not a decorator anymore! It's a decorator *factory method*, which makes it the 3rd order function.

## Requirement: Backward Compatibility

You feel quite happy with the easiness of the change, but a while later Dave, fellow member of another team, sends a rancorous message about you breaking his code in a dependant project. Yes, you did by making this modification. Have you noticed that the change in the signature made the usage a bit different?

```python
# before
@cache.cache_function_decorator
def expensive_function(*some_args, **some_kwargs): ...

#after
@cache.cache_function_decorator()  # (4)
def expensive_function(*some_args, **some_kwargs): ...
```

Sometimes you can negotiate or enforce compatibility changes on the dependant projects. And sometimes you can't. Let's assume that you can't. How to make calling the method non-obligatory? We'll modify the method again and use one more time the fact that [*functions are first-class citizens*](https://en.wikipedia.org/wiki/First-class_function) in Python.

```python
class Cache:
    ...

    def cache_function_decorator(
        self, f: Optional[Function] = None, *, expire: int = None  # (1)
    ) -> Union[Function, Callable[[Function], Function]]:  # (5)
        def cached_function(f: Function) -> Function:
            @functools.wraps(f)
            def wrapper(*args, **kwargs) -> Value:
                key = self.build_key(CallArgs(args, kwargs))
                if value_from_cache := self._engine.load(key) is not NotSet:
                    return value_from_cache
                value = f(*args, **kwargs)
                self._engine.store(key, value, expire=expire)
                return value

            return wrapper

        if f is None:  # (6)
            return cached_function
        else:
            return cached_function(f)
```

The conditioning `(6)` on the factory-method-level makes the method choose between having `f` as the main argument or not having. Unfortunately, this makes the signature of the method more complex `(5)`: either you get the decorator, or you get the actual wrapper. Right now, the decorator is both the 2nd and the 3rd order function. And that's not coincidental; this is the actual backward compatibility.

```python
(self: Cache, expire: int) -> Union[Function, Callable[[Function], Function]]
```

> NB: Notice that the argument `expire` has become [*keyword-only*](https://www.python.org/dev/peps/pep-3102/) `(1)`. This way, you defend against a simple yet fatal mistake of passing wrong arguments positionally.

Now you can do both of syntaxes and keep backward compatibility:

```python
# import-time
@cache.cache_function_decorator(expire=7)
def expensive_function(*some_args, **some_kwargs): ...

@cache.cache_function_decorator
def another_expensive_function(*some_args, **some_kwargs): ...
```

> NB: Many popular frameworks do the same trick. Take a look at the use-cases of the [`pytest.fixture`](https://docs.pytest.org/en/stable/fixture.html) decorator:
>
>```python
>@pytest.fixture
>def fixture_without_params(): ...
>
>@pytest.fixture(scope="session")
>def fixture_with_params(): ...
>```

## Conclusions

We have enhanced the caching feature to accept a kind of parametrization, making its method the 3rd order function.

If you want to see how this works in practice, take a look at our [working and tested example](fp02_method_as_decorator_factory.py).

[Next: Higher-Order Functions: Modifying Signatures ⇨](fp03_modifying_signatures.md)
