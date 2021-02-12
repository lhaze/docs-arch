import functools
import pytest
from typing import *

from .fp01_method_as_decorator import (
    Cache as FP01Cache,
    cache_engine,
    cache_memory,
    CallArgs,
    Function,
    NotSet,
    Value,
    cache_function_decorator_example,
)

CallArgsTransform = Callable[[CallArgs], CallArgs]
KwrgsTransform = Callable[..., Tuple[tuple, dict]]


class CallArgsCache(FP01Cache, Generic[Value]):
    def cache_function_decorator(
        self, f: Optional[Function] = None, *, expire: int = None, transform: CallArgsTransform = None  # (1)
    ) -> Callable[[Function], Function]:
        def cached_function(f: Function) -> Function:
            @functools.wraps(f)
            def wrapper(*args, **kwargs) -> Value:
                call_args = CallArgs(args, kwargs)
                if transform:
                    call_args = transform(call_args)  # (2)
                key = self.build_key(call_args)
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


class KwargsCache(FP01Cache, Generic[Value]):
    def cache_function_decorator(
        self, f: Optional[Function] = None, *, expire: int = None, transform: KwrgsTransform = None  # (1)
    ) -> Callable[[Function], Function]:
        def cached_function(f: Function) -> Function:
            @functools.wraps(f)
            def wrapper(*args, **kwargs) -> Value:
                if transform:
                    args, kwargs = transform(*args, **kwargs)  # (2)
                call_args = CallArgs(args, kwargs)
                key = self.build_key(call_args)
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


# Examples #

# This one conforms CallArgsTransform: Callable[[CallArgs], CallArgs]
def call_args_transform(call: CallArgs) -> CallArgs:
    # removing `self`
    args = call.args[1:]  # (4)
    # removing keyword-argument
    kwargs = dict(call.kwargs)  # (5)
    kwargs.pop("request", None)  # (6)
    return CallArgs(args=args, kwargs=kwargs)


# These two conform KwargsTransform: Callable[..., Tuple[tuple, dict]]
def kwargs_transform(self, request, *args, **kwargs) -> Tuple[tuple, dict]:
    return (args, kwargs)


lambda_transform = lambda self, request, *args, **kwargs: (args, kwargs)


class DIContainer:
    def get_request(self):
        return "request"


def inject_request_wrapping(container):
    def decorator(f: Callable):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            kwargs["request"] = container.get_request()
            return f(*args, **kwargs)

        return wrapper

    return decorator


def inject_request_partial(container):
    def decorator(f: Callable):
        return functools.wraps(f)(functools.partial(f, request=container.get_request()))

    return decorator


def cache_with_kwargs_transformation_example():
    cache = KwargsCache()
    container = DIContainer()

    class Foo:
        @cache.cache_function_decorator(expire=7)  # (3)
        def expensive_function(self, request, argument="argument"):
            ...

        @cache.cache_function_decorator(expire=7)  # (4)
        @inject_request_wrapping(container)
        def function_with_request(self, request, argument="argument"):
            return request, (self, argument)

    foo = Foo()
    foo.expensive_function("request", argument="argument")
    foo.function_with_request("request", argument="argument")
    foo.function_with_request()
    return foo


# Tests #


@pytest.fixture
def cache(cache_engine):
    cache = KwargsCache[str]()
    cache._engine = cache_engine
    return cache


@pytest.fixture
def cache(cache_engine):
    cache = KwargsCache[str]()
    cache._engine = cache_engine
    return cache


def test_call_args_transform():
    call = CallArgs(args=("self",), kwargs=dict(argument="argument", request="request"))
    assert call_args_transform(call) == CallArgs((), dict(argument="argument"))
    # this transform function won't do against ("self", "request", "argument")


def test_kwargs_transform():
    expected = ((), dict(dict(argument="argument")))
    assert expected == kwargs_transform("self", argument="argument", request="request")
    assert expected == kwargs_transform("self", "request", argument="argument")


def test_lambda_transform():
    expected = ((), dict(dict(argument="argument")))
    assert expected == lambda_transform("self", argument="argument", request="request")
    assert expected == lambda_transform("self", "request", argument="argument")


def test_injected_request():
    expected = ((), dict(dict(argument="argument")))
    assert expected == lambda_transform("self", argument="argument", request="request")
    assert expected == lambda_transform("self", "request", argument="argument")


def test_injecting_request_wrapper(cache):
    container = DIContainer()

    class Foo:
        @cache.cache_function_decorator
        @inject_request_wrapping(container)
        def function_with_request(self, request, argument="argument"):
            "My docstring."
            return (self, request, argument)

    foo = Foo()
    assert foo.function_with_request() == (foo, "request", "argument")
    assert foo.function_with_request.__qualname__ == (
        "test_injecting_request_wrapper.<locals>.Foo.function_with_request"
    )
    assert foo.function_with_request.__doc__ == "My docstring."


def test_injecting_request_partial(cache):
    container = DIContainer()

    class Foo:
        @cache.cache_function_decorator
        @inject_request_partial(container)
        def function_with_request(self, request, argument="argument"):
            "My docstring."
            return (self, request, argument)

    foo = Foo()
    assert foo.function_with_request() == (foo, "request", "argument")
    assert foo.function_with_request.__qualname__ == (
        "test_injecting_request_partial.<locals>.Foo.function_with_request"
    )
    assert foo.function_with_request.__doc__ == "My docstring."
