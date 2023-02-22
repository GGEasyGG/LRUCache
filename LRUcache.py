import time
from collections import OrderedDict
from typing import Any, Tuple, Optional, Callable


class HashKey(list):
    def __init__(self, tpl: Tuple[Any, ...]) -> None:
        super().__init__(tpl)
        self._hash: int = hash(tpl)

    def __hash__(self) -> int:  # type: ignore
        return self._hash


class LRUcache(OrderedDict):
    def __init__(self, cache_size: Optional[int]) -> None:
        super().__init__()
        self._cache_size: Optional[int] = cache_size

    def __getitem__(self, key: HashKey) -> Any:
        try:
            value = super().__getitem__(key)
        except KeyError:
            print(f'Error: There is no element with the key "{key}" in the cache!')
        else:
            if self._cache_size is not None:
                self.move_to_end(key)
            return value

    def __setitem__(self, key: HashKey, value: Any) -> None:
        if key in self:
            if self._cache_size is not None:
                self.move_to_end(key)

        super().__setitem__(key, value)

        if self._cache_size is not None:
            if len(self) > self._cache_size:
                oldest = next(iter(self))
                super().__delitem__(oldest)


def lru_cache(cache_size: Optional[int] = 10) -> Callable:
    def __lru_cache(function: Callable) -> Callable:
        if cache_size == 0:
            def wrapper(*args, **kwargs) -> Any:
                return function(*args, **kwargs)
        elif cache_size is not None and cache_size < 0:
            raise ValueError("The cache size cannot be negative")
        else:
            cache = LRUcache(cache_size)

            def wrapper(*args, **kwargs) -> Any:
                key = HashKey(args)

                if key in cache:
                    return cache[key]
                else:
                    result = function(*args, **kwargs)
                    cache[key] = result
                    return result

        return wrapper

    return __lru_cache


def timed(function: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        time_start = time.time()
        result = function(*args, **kwargs)
        time_end = time.time()

        print('Function name: {}\n'
              '  Returned value: {}\n'
              '  Execution time: {:.3f} ms\n'.format(function.__name__, result, (time_end - time_start) * 1000))

        return result

    return wrapper
