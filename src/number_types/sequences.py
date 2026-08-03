"""Finite prefixes of classical integer sequences."""

from collections.abc import Callable


def sequence_values(formula: Callable[[int], int], limit: int) -> set[int]:
    """Evaluate an increasing positive-integer formula up to ``limit``."""
    values: set[int] = set()
    index = 1
    while (value := formula(index)) <= limit:
        values.add(value)
        index += 1
    return values


def fibonacci_numbers(limit: int) -> set[int]:
    """Return positive Fibonacci numbers not exceeding ``limit``."""
    values: set[int] = set()
    first, second = 1, 2
    while first <= limit:
        values.add(first)
        first, second = second, first + second
    return values


def catalan_numbers(limit: int) -> set[int]:
    """Return Catalan numbers not exceeding ``limit``."""
    values: set[int] = set()
    index, catalan = 0, 1
    while catalan <= limit:
        values.add(catalan)
        catalan = catalan * 2 * (2 * index + 1) // (index + 2)
        index += 1
    return values


def pell_numbers(limit: int) -> set[int]:
    """Return positive Pell numbers not exceeding ``limit``."""
    values: set[int] = set()
    previous, current = 0, 1
    while current <= limit:
        values.add(current)
        previous, current = current, 2 * current + previous
    return values
