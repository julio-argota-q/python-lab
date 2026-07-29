Exercise 1 — Immutable Vector

Implement an immutable numerical Vector class similar to a
lightweight NumPy vector.

Features: - Store values efficiently (e.g. array(‘d’)). - Immutable
after construction. - Implement: - len - iter - getitem (including
slicing) - repr - eq - hash - Arithmetic: - vector + vector - vector -
vector - scalar multiplication - dot product - JSON serialization. -
from_string() constructor. - Validate dimensions and operand types. -
Raise appropriate exceptions for invalid operations.

Suggested tests: - Equality and hashing. - Slicing returns Vector. -
Arithmetic correctness. - Dimension mismatch. - Immutability.