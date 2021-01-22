import dataclasses
import functools
import pytest
import typing as t
from unittest import mock

Key = t.NewType("Key", str)
Value = t.TypeVar("Value")
Function = t.Callable[..., Value]
NotSet = mock.sentinel.NotSet


@dataclasses.dataclass(frozen=True)
class Call:
    args: t.Tuple
    kwargs: t.Dict[str, t.Any]


class CacheEngine(t.Generic[Value]):
    def load(self, key: Key) -> Value:
        ...

    def store(self, key: Key, value: Value, expire: int = None) -> None:
        ...


class Cache(t.Generic[Value]):
    """
    This class should know how to cache things.
    """

    _engine: CacheEngine

    def build_key(self, call: Call) -> Key:
        return str(call)

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

    def cache_function_decorator_with_params(self, expire: int = None) -> t.Callable[[Function], Function]:
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

        return cached_function


# Examples #


def cache_function_decorator_example():
    # configuration-time
    cache = Cache()

    # import-time
    @cache.cached  # (6)
    def expensive_function(*some_args, **some_kwargs):
        """My docstring."""

    # usage-time
    expensive_function("foo")  # now I'm running the computations...
    expensive_function("foo")  # ... and now I'm not
    expensive_function("bar")  # ... and now again I'm running my computations because arguments differ
    assert expensive_function.__name__ == "expensive_function"  # (7)
    assert expensive_function.__doc__ == "My docstring."  # (7)


# Tests #


@pytest.fixture
def cache_memory():
    return {}


@pytest.fixture
def cache_engine(cache_memory: dict):
    mocked = mock.Mock(spec=CacheEngine)
    mocked.load.side_effect = lambda key: cache_memory.get(key, NotSet)
    mocked.store.side_effect = lambda key, value, **kwargs: cache_memory.__setitem__(key, value)
    return mocked


@pytest.fixture
def cache(cache_engine):
    cache = Cache()
    cache._engine = cache_engine
    return cache


def test_build_key(cache):
    args = ()
    kwargs = {}
    assert cache.build_key(Call(args, kwargs)) == "Call(args=(), kwargs={})"


def test_decorated_function_identity(cache):
    @cache.cache_function_decorator
    def foo(bar):
        """My docstring."""
        return "result"

    assert foo.__name__ == "foo"
    assert foo.__doc__ == "My docstring."


def test_cache_function_decorator(cache: Cache, cache_engine: mock.Mock, cache_memory: dict):
    @cache.cache_function_decorator
    def foo(bar):
        return "result"

    foo("bar")
    foo("bar")
    assert cache_engine.load.call_args_list == [
        mock.call("Call(args=('bar',), kwargs={})"),
        mock.call("Call(args=('bar',), kwargs={})"),
    ]
    cache_engine.store.assert_called_once_with("Call(args=('bar',), kwargs={})", "result")
    assert cache_memory["Call(args=('bar',), kwargs={})"] == "result"


def test_cache_function_decorator_with_params(cache: Cache, cache_engine: mock.Mock, cache_memory: dict):
    @cache.cache_function_decorator_with_params(expire=10)
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