#!/usr/bin/env python3
"""
Redis basic: module providing a Cache class to store and retrieve values,
with call count tracking, call history, and a replay utility.

- count_calls: increments a per-method counter using INCR.
- call_history: records inputs and outputs in Redis lists.
- replay: pretty-prints the history of a method's calls.
- Cache.get / get_str / get_int: retrieve values with optional conversion.
"""
from typing import Any, Callable, Optional, TypeVar, Union
from uuid import uuid4
import functools

import redis

T = TypeVar("T")


def count_calls(method: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to count how many times a method is called.

    It uses Redis INCR on the method's qualified name (__qualname__).
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that stores inputs and outputs of a method in Redis.

    For a method with qualified name QN, two lists are used:
    - f"{QN}:inputs"  -> rpush(str(args)) for each call (kwargs ignored)
    - f"{QN}:outputs" -> rpush(result) after the call
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        qualname = method.__qualname__
        in_key = f"{qualname}:inputs"
        out_key = f"{qualname}:outputs"
        # Normalize positional args to a string representation
        self._redis.rpush(in_key, str(args))
        result = method(self, *args, **kwargs)
        # Store raw output; Redis accepts str/bytes/int/float
        self._redis.rpush(out_key, result)
        return result

    return wrapper


def replay(method: Callable[..., Any]) -> None:
    """Display the call history of a method recorded by call_history/count_calls.

    It reads:
      - the total call count from key "<qualname>"
      - inputs from list "<qualname>:inputs"
      - outputs from list "<qualname>:outputs"
    and prints them in a readable format.
    """
    qualname = method.__qualname__

    # Try to use the same Redis instance when method is bound to a Cache
    rds = getattr(getattr(method, "__self__", None), "_redis", None)
    if rds is None:
        rds = redis.Redis()

    # Total calls
    raw_count = rds.get(qualname)
    count = int(raw_count) if raw_count is not None else 0
    print(f"{qualname} was called {count} times:")

    # Inputs and outputs
    in_key = f"{qualname}:inputs"
    out_key = f"{qualname}:outputs"
    inputs = rds.lrange(in_key, 0, -1)
    outputs = rds.lrange(out_key, 0, -1)

    for raw_args, raw_out in zip(inputs, outputs):
        args_str = raw_args.decode("utf-8")
        out_str = raw_out.decode("utf-8")
        print(f"{qualname}(*{args_str}) -> {out_str}")


class Cache:
    """Simple cache wrapper over a Redis client with call tracking."""

    def __init__(self) -> None:
        """Initialize the Redis client and flush the database."""
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis under a random UUID key and return the key."""
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable[[bytes], T]] = None
    ) -> Optional[Union[bytes, T]]:
        """Retrieve a value by key and optionally convert its type.

        If the key does not exist, return None. Otherwise return the raw
        bytes from Redis, or the value transformed by ``fn`` when provided.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a UTF-8 decoded string for the given key, or None."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))  # type: ignore[return-value]

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer for the given key, or None."""
        return self.get(key, fn=int)  # type: ignore[return-value]
