"""Some utility functions used throughout the library.
Copyright (c) Kiruse 2021. See license in LICENSE."""
from typing import *

T = TypeVar('T')

def isempty(iterable: Iterable) -> bool:
    try:
        return len(iterable) == 0
    except TypeError:
        pass
    
    try:
        next(iter(iterable))
        return False
    except StopIteration:
        return True

def shift(lst: List[T]) -> T:
    item = lst[0]
    del lst[0]
    return item

def unshift(lst: List[T], item: T) -> List[T]:
    lst.insert(0, item)
    return lst
