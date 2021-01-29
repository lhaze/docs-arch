import functools
import pytest
import typing as t
from unittest import mock

from .fp01_method_as_decorator import (
    Cache as FP01Cache,
    CallArgs,
    Function,
    NotSet,
    Value,
)

CallArgsTransform = t.Callable[[CallArgs], CallArgs]


class Cache(FP01Cache, t.Generic[Value]):
    def cache_function_decorator(
        self, f: t.Optional[Function] = None, *, expire: int = None, tramsform: CallArgsTransform = None  # (1)
    ) -> t.Callable[[Function], Function]:
        def cached_function(f: Function) -> Function:
            @functools.wraps(f)
            def wrapper(*args, **kwargs) -> Value:
                call_args = CallArgs(args, kwargs)
                if tramsform:
                    call_args = tramsform(call_args)  # (2)
                key = self.build_key(call_args)
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
    class Foo:
        @cache.cache_function_decorator(expire=7)  # (3)
        def expensive_function(self, *some_args, **some_kwargs):
            ...

        @cache.cache_function_decorator(expire=7)  # (3)
        def expensive_function_with_request(self, request, **some_kwargs):
            ...
