# import unittest
# from src.config_utils.logger import setup_logger
#
#
# class CustomTestResult(unittest.TestResult):
#     def startTest(self, test):
#         logger = setup_logger(test.__class__.__module__)
#         logger.debug(f"Starting test {test._testMethodName}")
#         super().startTest(test)
#
#     def stopTest(self, test):
#         logger = setup_logger(test.__class__.__module__)
#         logger.debug(f"Stopping test {test._testMethodName}")
#         super().stopTest(test)
#
#
# def custom_test_runner(*args, **kwargs):
#     return unittest.TextTestRunner(resultclass=CustomTestResult, *args, **kwargs)
#
#
# unittest.defaultTestLoader.testRunner = custom_test_runner