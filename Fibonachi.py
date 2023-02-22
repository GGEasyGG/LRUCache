from LRUcache import *


@timed
def fib_with_cache(n: int) -> int:
    @lru_cache(cache_size=20)
    def fib(i: int) -> int:
        if i < 2:
            return i

        return fib(i-1) + fib(i-2)

    return fib(n)


@timed
def fib_without_cache(n: int) -> int:
    def fib(i: int) -> int:
        if i < 2:
            return i

        return fib(i-1) + fib(i-2)

    return fib(n)


if __name__ == "__main__":
    print()
    fib_without_cache(30)
    fib_with_cache(30)
