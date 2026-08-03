"""Build the category catalog used by the visualization."""

from dataclasses import dataclass
from math import isqrt, log2

from .predicates import (
    digit_sum, is_happy, is_kaprekar, is_prime, is_semiprime, is_smith,
    is_sphenic, lucky_numbers, proper_divisor_sum,
)
from .sequences import catalan_numbers, fibonacci_numbers, pell_numbers, sequence_values


@dataclass(frozen=True, slots=True)
class Category:
    """A named finite number class and its display color."""

    title: str
    values: frozenset[int]
    color: str


def build_categories(limit: int = 100) -> list[Category]:
    """Return the 34 number categories restricted to ``1 <= n <= limit``."""
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("limit must be a positive integer")
    numbers = set(range(1, limit + 1))
    squares = {base**2 for base in range(1, isqrt(limit) + 1)}
    cubes = {base**3 for base in range(1, limit + 1) if base**3 <= limit}
    maximum_exponent = int(log2(limit)) if limit > 1 else 1
    powers = {base**exponent for base in range(2, limit + 1)
              for exponent in range(2, maximum_exponent + 1) if base**exponent <= limit}
    data = [
        ("Natural Numbers", numbers), ("Odd Numbers", {n for n in numbers if n % 2}),
        ("Even Numbers", {n for n in numbers if n % 2 == 0}),
        ("Multiples of 3", {n for n in numbers if n % 3 == 0}),
        ("Multiples of 5", {n for n in numbers if n % 5 == 0}),
        ("Multiples of 7", {n for n in numbers if n % 7 == 0}),
        ("Multiples of 10", {n for n in numbers if n % 10 == 0}),
        ("Prime Numbers", {n for n in numbers if is_prime(n)}),
        ("Composite Numbers", {n for n in numbers if n > 1 and not is_prime(n)}),
        ("Semiprime Numbers", {n for n in numbers if is_semiprime(n)}),
        ("Square Numbers", squares), ("Cube Numbers", cubes), ("Perfect Powers", powers),
        ("Triangular Numbers", sequence_values(lambda n: n * (n + 1) // 2, limit)),
        ("Tetrahedral Numbers", sequence_values(lambda n: n * (n + 1) * (n + 2) // 6, limit)),
        ("Square Pyramidal Numbers", sequence_values(lambda n: n * (n + 1) * (2*n + 1) // 6, limit)),
        ("Pentagonal Numbers", sequence_values(lambda n: n * (3*n - 1) // 2, limit)),
        ("Hexagonal Numbers", sequence_values(lambda n: n * (2*n - 1), limit)),
        ("Perfect Numbers", {n for n in numbers if n > 1 and proper_divisor_sum(n) == n}),
        ("Abundant Numbers", {n for n in numbers if proper_divisor_sum(n) > n}),
        ("Deficient Numbers", {n for n in numbers if proper_divisor_sum(n) < n}),
        ("Fibonacci Numbers", fibonacci_numbers(limit)),
        ("Decimal Harshad Numbers", {n for n in numbers if n % digit_sum(n) == 0}),
        ("Sphenic Numbers", {n for n in numbers if is_sphenic(n)}),
        ("Smith Numbers", {n for n in numbers if is_smith(n)}),
        ("Binary Palindromic Numbers", {n for n in numbers if (b := bin(n)[2:]) == b[::-1]}),
        ("Decimal Palindromic Numbers", {n for n in numbers if str(n) == str(n)[::-1]}),
        ("Happy Numbers", {n for n in numbers if is_happy(n)}),
        ("Lucky Numbers", lucky_numbers(limit)),
        ("Evil Numbers", {n for n in numbers if bin(n).count("1") % 2 == 0}),
        ("Automorphic Numbers", {n for n in numbers if str(n*n).endswith(str(n))}),
        ("Kaprekar Numbers", {n for n in numbers if is_kaprekar(n)}),
        ("Catalan Numbers", catalan_numbers(limit)), ("Pell Numbers", pell_numbers(limit)),
    ]
    palette = [f"#{value:06x}" for value in range(0xE53935, 0xE53935 + len(data) * 9973, 9973)]
    return [Category(title, frozenset(values), palette[index]) for index, (title, values) in enumerate(data)]
