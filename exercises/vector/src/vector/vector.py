
'''
    vector/vector.py

    Implement an immutable numerical Vector class similar to a
    lightweight NumPy vector.

    Features: - Store values efficiently. - Immutable
    after construction. - Implement: - len - iter - getitem (including
    slicing) - repr - eq - hash - Arithmetic: - vector + vector - vector -
    vector - scalar multiplication - dot product - JSON serialization. -
    from_string() constructor. - Validate dimensions and operand types. -
    Raise appropriate exceptions for invalid operations.
'''

import json
from array import array
from collections.abc import Iterable, Iterator


class Vector:
    __slots__ = ('_components',)

    def __init__(self, components:Iterable[float])-> None:
        self._components = tuple(array('d', components))

    def __len__(self) -> int:
        return len(self._components)

    def __getitem__(self, key: int | slice) -> 'Vector' | float:

        if isinstance(key, slice):
            return Vector(self._components[key])
        
        return self._components[key]

    def __iter__(self) -> Iterator[float]:
        return iter(self._components)

    def __add__(self, other:'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            return NotImplemented
        self._check_dim(other)
        return Vector([ c1 + c2 for c1, c2 in zip(self._components, other._components)])

    def __sub__(self, other:'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            return NotImplemented
        self._check_dim(other)
        return Vector([ c1 - c2 for c1, c2 in zip(self._components, other._components)])

    def __rmul__(self, scalar:float) -> 'Vector':
        if not isinstance(scalar, (int,float)):
            raise TypeError('This operation need a scalar')    
        return Vector([scalar * c  for c in self._components])

    def __mul__(self, scalar:float) -> 'Vector':
        if not isinstance(scalar, (int,float)):
            raise TypeError('This operation need a scalar')
        return Vector([scalar * c  for c in self._components])

    def __matmul__(self, other:'Vector') -> float:
        self._check_dim(other)
        return sum([c1 * c2 for c1,c2 in zip(other._components, self._components)])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        
        return self._components == other._components

    def __hash__(self) -> int:
        return hash(self._components)

    def __repr__(self) -> str:
        return f'Vector({', '.join(str(c) for c in self._components)})'

    def _check_dim(self, other:'Vector') -> None:
        if len(other) != len(self):
            raise ValueError('Vectors need to be have same dimension')

    def to_json(self) -> str:
        return json.dumps(list(self._components))

    @classmethod
    def from_string(cls, components:str) -> 'Vector':
        return Vector([float(c.strip()) for c in components.split(',') if c.strip()])
    