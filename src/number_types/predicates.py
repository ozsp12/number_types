"""Predicates and arithmetic helpers for positive integers."""

from math import isqrt


def _require_positive(n: int) -> None:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")


def is_prime(n: int) -> bool:
    """Return whether ``n`` has exactly two positive divisors."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % divisor for divisor in range(3, isqrt(n) + 1, 2))


def prime_factors(n: int) -> list[int]:
    """Return the prime factorization of ``n`` with multiplicity."""
    _require_positive(n)
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def digit_sum(n: int) -> int:
    """Return the sum of the base-ten digits of a nonnegative integer."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n must be a nonnegative integer")
    return sum(int(digit) for digit in str(n))


def proper_divisor_sum(n: int) -> int:
    """Return the sum of positive divisors strictly smaller than ``n``."""
    _require_positive(n)
    if n == 1:
        return 0
    total = 1
    for divisor in range(2, isqrt(n) + 1):
        if n % divisor == 0:
            quotient = n // divisor
            total += divisor
            if quotient != divisor:
                total += quotient
    return total


def is_semiprime(n: int) -> bool:
    """Return whether ``n`` is a product of two primes, with multiplicity."""
    return isinstance(n, int) and n >= 4 and len(prime_factors(n)) == 2


def is_sphenic(n: int) -> bool:
    """Return whether ``n`` is a product of three distinct primes."""
    if not isinstance(n, int) or n < 30:
        return False
    factors = prime_factors(n)
    return len(factors) == 3 and len(set(factors)) == 3


def is_smith(n: int) -> bool:
    """Return whether composite ``n`` has equal digit and factor digit sums."""
    if not isinstance(n, int) or n < 4 or is_prime(n):
        return False
    return digit_sum(n) == sum(digit_sum(factor) for factor in prime_factors(n))


def is_happy(n: int) -> bool:
    """Return whether iterated squared-digit sums reach one."""
    if not isinstance(n, int) or n < 1:
        return False
    visited: set[int] = set()
    while n != 1 and n not in visited:
        visited.add(n)
        n = sum(int(digit) ** 2 for digit in str(n))
    return n == 1


def lucky_numbers(limit: int) -> set[int]:
    """Return classical lucky numbers not exceeding ``limit``."""
    if not isinstance(limit, int) or limit < 1:
        return set()
    values = list(range(1, limit + 1, 2))
    index = 1
    while index < len(values):
        step = values[index]
        if step > len(values):
            break
        values = [value for position, value in enumerate(values, 1) if position % step]
        index += 1
    return set(values)


def is_kaprekar(n: int) -> bool:
    """Return whether ``n`` satisfies the standard base-ten Kaprekar split."""
    if not isinstance(n, int) or n < 1:
        return False
    if n == 1:
        return True
    left, right = divmod(n * n, 10 ** len(str(n)))
    return right > 0 and left + right == n
