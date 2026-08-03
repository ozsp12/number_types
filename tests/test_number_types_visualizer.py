"""Regression tests for the mathematical catalog."""

import unittest

from number_types_visualizer import NumberTypesVisualizer


class NumberTypesVisualizerTests(unittest.TestCase):
    def setUp(self):
        self.visualizer = NumberTypesVisualizer()
        self.categories = {category.title: category.values for category in self.visualizer.categories}

    def test_catalog_contains_34_categories(self):
        self.assertEqual(len(self.visualizer.categories), 34)

    def test_reference_number_classes(self):
        self.assertEqual(len(self.categories["Prime Numbers"]), 25)
        self.assertEqual(self.categories["Perfect Numbers"], {6, 28})
        self.assertEqual(self.categories["Pell Numbers"], {1, 2, 5, 12, 29, 70})

    def test_factorization_and_special_predicates(self):
        self.assertEqual(self.visualizer.prime_factors(72), [2, 2, 2, 3, 3])
        self.assertTrue(self.visualizer.is_happy(19))
        self.assertTrue(self.visualizer.is_kaprekar(45))


if __name__ == "__main__":
    unittest.main()
