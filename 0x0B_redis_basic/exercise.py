#!/usr/bin/env python3
"""Redis basic: module providing a Cache class to store and retrieve values.

This module defines a ``Cache`` class that connects to a local Redis
server and offers a ``store`` method to persist arbitrary data under a
randomly generated key. It also provides retrieval helpers that can
recover the original Python type via an optional conversion callable.
"""
from __future__ import annotations

from typing import Callable, Optional, TypeVar, Union
from uuid import uuid4

import redis

T = TypeVar("T")


class Cache:
    """Simple cache wrapper over a Redis client.

    Upon initialization, it creates a Redis client connected to the
    default local server and flushes the current database to provide a
    clean state for exercises.
    """

    def __init__(self) -> None:
        """Initialize the cache with a fresh Redis database.

        A private ``_redis`` attribute holds the ``redis.Redis`` client
        instance. The database is cleared using ``flushdb`` so that each
        new ``Cache`` starts from an empty state.
        """
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store ``data`` in Redis under a random UUID key.

        Args:
            data: The value to persist. May be ``str``, ``bytes``,
                ``int`` or ``float``.

        Returns:
            The string key used to store the value in Redis.

        The key is generated using :func:`uuid.uuid4` and converted to a
        string. The raw ``data`` is saved with ``SET`` and no additional
        serialization is performed.
        """
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable[[bytes], T]] = None
    ) -> Optional[Union[bytes, T]]:
        """Retrieve a value by ``key`` and optionally convert its type.

        Redis returns raw ``bytes`` for string-like values. If ``fn`` is
        provided, it will be applied to the raw bytes to convert them
        back to the desired Python type.

        Args:
            key: Redis key to retrieve.
            fn: Optional callable that accepts the raw ``bytes`` from
                Redis and returns a converted value.

        Returns:
            ``None`` if the key does not exist; otherwise either the raw
            ``bytes`` value or the converted value if ``fn`` is given.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a UTF-8 decoded string value for ``key``.

        Returns ``None`` if the key does not exist.
        """
        data = self.get(key, fn=lambda d: d.decode("utf-8"))
        return data  # type: ignore[return-value]

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer value for ``key``.

        Returns ``None`` if the key does not exist. The conversion uses
        Python's ``int`` built-in on the raw bytes, which handles ASCII
        representations such as ``b"123"``.
        """
        data = self.get(key, fn=int)
        return data  # type: ignore[return-value]
