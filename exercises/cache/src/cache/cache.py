from functools import wraps
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class CacheInfo:
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0
    current_size: int = 0

    def clear(self) -> None:
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0
        self.current_size = 0

class Cache:
    info: CacheInfo
    ttl: float | None = None
    maxsize: int = 128
    cahe: OrderedDict

    def __init__(self,ttl: float | None = None, maxsize: int = 12) -> None:

        if ttl is not None and ttl < 0:
            raise ValueError('The value of ttl must be bigger than zero')

        if maxsize < 0:
            raise ValueError('The value of maxsize must be bigger than zero')

        self.ttl = ttl
        self.maxsize = maxsize
        self.cahe = OrderedDict()

    def __call__(self, func:Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key2 = tuple(args)
            key1 = tuple(v for _, v in sorted(kwargs.items()))
            print(f'before function:{key1}, {key2}')
            result = func(*args, **kwargs)
            print(f'after function:{result}')
            return result

        return wrapper

@Cache(ttl=3, maxsize=128)
def new_sum(x:int, y:int=1, *, a:int=3, b:int=1) -> int:
    return x + y + a + b

if __name__ == '__main__':
    new_sum(3,4, a=2)
    new_sum(3,4, b=2)