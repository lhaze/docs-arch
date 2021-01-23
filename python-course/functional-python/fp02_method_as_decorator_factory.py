import functools
import pytest
import typing as t
from unittest import mock

from fp01_method_as_decorator import (
    Cache as FP01Cache,
    cache_engine,
    cache_memory,
    Call,
    Function,
    NotSet,
    Value,
)


class Cache(FP01Cache, t.Generic[Value]):
    def cache_function_decorator(
        self, f: t.Optional[Function] = None, *, expire: int = None  # (1)
    ) -> t.Callable[[Function], Function]:  # (2)
        def cached_function(f: Function) -> Function:
            @functools.wraps(f)
            def wrapper(*args, **kwargs) -> Value:
                key = self.build_key(Call(args, kwargs))
                if value_from_cache := self._engine.load(key) is not NotSet:
                    return value_from_cache
                value = f(*args, **kwargs)
                self._engine.store(key, value, expire=expire)
                return value

            return wrapper

        if f is None:  # (5)
            return cached_function
        else:
            return cached_function(f)


# Examples #


def cache_function_decorator_with_params_example():
    # configuration-time
    cache = Cache()

    # import-time
    @cache.cache_function_decorator(expire=7)  # (3)
    def expensive_function(*some_args, **some_kwargs):
        ...

    @cache.cache_function_decorator()  # (4)
    def another_expensive_function(*some_args, **some_kwargs):
        ...


# Tests #


@pytest.fixture
def cache(cache_engine):
    cache = Cache[str]()
    cache._engine = cache_engine
    return cache


def test_cache_function_decorator_with_params(cache: Cache[str], cache_engine: mock.Mock, cache_memory: dict):
    @cache.cache_function_decorator(expire=10)
    def foo(bar):
        return "result"

    foo("bar")
    foo("bar")
    assert cache_engine.load.call_args_list == [
        mock.call("Call(args=('bar',), kwargs={})"),
        mock.call("Call(args=('bar',), kwargs={})"),
    ]
    cache_engine.store.assert_called_once_with("Call(args=('bar',), kwargs={})", "result", expire=10)
    assert cache_memory["Call(args=('bar',), kwargs={})"] == "result"


def test_cache_function_decorator_without_params(cache: Cache[str], cache_engine: mock.Mock, cache_memory: dict):
    @cache.cache_function_decorator
    def foo(bar):
        return "result"

    foo("bar")
    foo("bar")
    assert cache_engine.load.call_args_list == [
        mock.call("Call(args=('bar',), kwargs={})"),
        mock.call("Call(args=('bar',), kwargs={})"),
    ]
    cache_engine.store.assert_called_once_with("Call(args=('bar',), kwargs={})", "result", expire=None)
    assert cache_memory["Call(args=('bar',), kwargs={})"] == "result"
