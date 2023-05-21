import unittest
from tests.custom_test_runner import CustomTestRunner

module_to_test = "tests/integration/scenarios/test_mosquito_vs_cricket"
class_to_test = "TestMosquitoVsCricket"
method_to_test = "test4_Mosquito_v_1_Cricket_Sequentially"

module_to_test = module_to_test.replace("/", ".")

test_name = ".".join((module_to_test, class_to_test, method_to_test)).rstrip(".")
print(test_name)
# Runs specific tests and utilizes logging

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromName(test_name)
    result = CustomTestRunner().run(suite)



# Discovers and runs all tests and utilizes logging

# if __name__ == '__main__':
#     suite = unittest.TestLoader().discover('tests')
#     result = CustomTestRunner().run(suite)
