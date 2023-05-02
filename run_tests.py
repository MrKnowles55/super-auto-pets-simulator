import unittest
from tests.custom_test_runner import CustomTestRunner

if __name__ == '__main__':
    suite = unittest.TestLoader().discover('tests')
    result = CustomTestRunner().run(suite)
