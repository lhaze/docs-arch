### Functional Python by Examples

This series of articles shows plain examples of using functional programming in Python. We won't stop at building a parametrized decorator, as most of the examples on the web do. Instead, we will move on step by step away from procedural and object programming. Exploring common problems of development, we will solve them using features of functional syntax in Python.

- [Part 3. Higher-Order Functions: Modifying Signatures](#part-3-higher-order-functions-modifying-signatures)
  - [The Context](#the-context)
  - [Requirement: Removing an Argument -- Decorating a Method](#requirement-removing-an-argument----decorating-a-method)
    - [An Object Transformation](#an-object-transformation)
    - [Unpacking Operator](#unpacking-operator)
  - [Requirement: Fixing an Attribute -- Dependency Injection](#requirement-fixing-an-attribute----dependency-injection)
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

## Requirement: Removing an Argument -- Decorating a Method

The next day, the yet known fellow team member, Dave, shows up to warn us, that our caching feature doesn't work. They're using the decorator and nothing happens -- all calls are executed. Let's look at how Dave is doing it:

```python
cache = Cache()

class Service:

    @cache.cache_function_decorator(expire=7)
    def expensive_method(self, *some_args, **some_kwargs):  # (2)
        ...

def process(cls):
    instance = Service()  # (3)
    instance.expensive_function(*some_args)
```

Oh, bugger! You haven't known, they are going to decorate a method of a short-lifespaned object. Instances of `Service` are created only for a while `(3)`, and yet they participate in creating the set of arguments of the call `(2)`. This means each time the `expensive_method` is called, cache is differentiating the calls with `self` argument. Not good. It seems you should provide a way for the cache to chop off some arguments of the call while regarding building the key for the call `(1)`. You probably want to chop of `self` argument, but there may be more arguments that are [*volatile*](https://en.wikipedia.org/wiki/Volatile_(computer_programming)) and aren't supposed to be regarded to the cache key.

> NB: Quite common example of a *volatile* value is a `request` instance to a web server application. You probably don't want to cache things only for the current request.

> NB2: Please note, that the following 3 calls are differentiated by the cache. Although they have the same Python semantics, yet the calls are syntactically different:
>
> ```python
> def foo(arg1, arg2, arg3='arg3'):
>   ...
>
> foo("arg1", "arg2", arg3="arg3")
> foo("arg1", arg2="arg2", arg3="arg3")
> foo(arg1="arg1", arg2="arg2") 
> ```
>
> The way the cache is written, it will treat each of these calls separately, because values of their `args` & `kwargs` are literally different. It's a conscious decision -- analyzing functions' signatures to build semantic equality would bring us to dealing with corner-cases.

Ok, let's generalize the problem a bit. We are looking for a class of functions that transform the arguments. We can do this in two ways:

### An Object Transformation

In previous parts, we created `CallArgs` [dataclass](https://realpython.com/python-data-classes/) (a class for keeping descriptive data) for the arguments of a call. Let's look how a transformation of a class could look like using this structure. We're looking for a `(CallArgs) -> CallArgs` function, that strips down first positional argument (`self`) `(4)` and takes out the one named `request` as well `(6)`.

```python
def call_args_transform(call: CallArgs) -> CallArgs:
    # removing `self`
    args = call.args[1:]  # (4)
    # removing keyword-argument
    kwargs = dict(call.kwargs)  # (5)
    kwargs.pop("request", None)  # (6)
    return CallArgs(args=args, kwargs=kwargs)
```

> NB: As a sidenote, please note that we make a [shallow copy](https://en.wikipedia.org/wiki/Object_copying#Shallow_copy) of `CallArgs.kwargs` attribute by a copy constructor of `dict` `(5)`. If we hadn't, we would mutate a part of the structure passed as the argument. It is a classic example of a [side effect](https://en.wikipedia.org/wiki/Side_effect_(computer_science)) and [later on]() we learn why it's a bad practice and how to avoid it.

> NB2: preparing `CallArgs.args` at `(4)` doesn't need such a precaution, because `args: tuple` is an [immutable](https://en.wikipedia.org/wiki/Immutable_object#Weak_vs_strong_immutability) structure. [Later on]() we will learn how immutability of values can improve your code.

It works... but not so well how like. Look at these examples of usage:

```python
cache = CallArgsCache()

class Foo:
    @cache.cache_function_decorator(transform=call_args_transform)  # (6)
    def expensive_function(self, request, argument="argument")):
        ...

foo = Foo()
foo.expensive_function(argument="argument", request="request")
```

### Unpacking Operator

Python has these unpacking operators: `*` and `**`. They serve to

or `args/kwargs` into another set

```python
(*args, **kwargs) -> Tuple[tuple, dict]

# for example

lambda self, request, *args, **kwargs: (args, kwargs)  # (6)
```

## Requirement: Fixing an Attribute -- Dependency Injection

(...)

## Conclusions

(...)

If you want to see how this works in practice, take a look at our [working and tested example](fp03_modifying_signatures.py).

[Next: Higher-Order Functions: Composing Decorators ⇨](fp04_composing_decorators.md)
