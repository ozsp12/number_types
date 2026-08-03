import unittest

from number_types import (
    build_categories, catalan_numbers, fibonacci_numbers, is_happy, is_kaprekar,
    is_prime, is_semiprime, is_smith, is_sphenic, lucky_numbers, pell_numbers,
    prime_factors, proper_divisor_sum,
)


class PredicateTests(unittest.TestCase):
    def test_prime_and_factorization(self):
        self.assertTrue(is_prime(97))
        self.assertFalse(is_prime(1))
        self.assertEqual(prime_factors(72), [2, 2, 2, 3, 3])

    def test_arithmetic_classes(self):
        self.assertEqual(proper_divisor_sum(28), 28)
        self.assertTrue(is_semiprime(49))
        self.assertTrue(is_sphenic(30))
        self.assertTrue(is_smith(22))
        self.assertTrue(is_happy(19))
        self.assertTrue(is_kaprekar(45))
        self.assertEqual(sorted(lucky_numbers(20)), [1, 3, 7, 9, 13, 15])

    def test_sequences(self):
        self.assertEqual(fibonacci_numbers(100), {1, 2, 3, 5, 8, 13, 21, 34, 55, 89})
        self.assertEqual(catalan_numbers(100), {1, 2, 5, 14, 42})
        self.assertEqual(pell_numbers(100), {1, 2, 5, 12, 29, 70})

    def test_catalog(self):
        categories = build_categories(100)
        self.assertEqual(len(categories), 34)
        by_name = {category.title: category.values for category in categories}
        self.assertEqual(len(by_name["Prime Numbers"]), 25)
        self.assertEqual(by_name["Perfect Numbers"], {6, 28})
        self.assertEqual(by_name["Square Numbers"], {1, 4, 9, 16, 25, 36, 49, 64, 81, 100})


if __name__ == "__main__":
    unittest.main()
