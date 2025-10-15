"""
Unit tests for func.py
Converted from Idris2 func.idr
"""

import unittest
from func import api_function, _helper_function


class TestHelperFunction(unittest.TestCase):
    """Tests for the private helper function"""

    def test_helper_function_positive(self):
        """Test helper function with positive number"""
        self.assertEqual(_helper_function(5), 6)

    def test_helper_function_zero(self):
        """Test helper function with zero"""
        self.assertEqual(_helper_function(0), 1)

    def test_helper_function_negative(self):
        """Test helper function with negative number"""
        self.assertEqual(_helper_function(-3), -2)


class TestApiFunction(unittest.TestCase):
    """Tests for the public API function"""

    def test_api_function_positive(self):
        """Test API function with positive number"""
        # (5 + 1) * 2 = 12
        self.assertEqual(api_function(5), 12)

    def test_api_function_zero(self):
        """Test API function with zero"""
        # (0 + 1) * 2 = 2
        self.assertEqual(api_function(0), 2)

    def test_api_function_negative(self):
        """Test API function with negative number"""
        # (-3 + 1) * 2 = -4
        self.assertEqual(api_function(-3), -4)

    def test_api_function_large_number(self):
        """Test API function with large number"""
        # (100 + 1) * 2 = 202
        self.assertEqual(api_function(100), 202)

    def test_api_function_type(self):
        """Test API function returns correct type"""
        result = api_function(5)
        self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
