import unittest
from src.config_utils.logger import setup_logger


class CustomTestRunner(unittest.TextTestRunner):
    def run(self, test):
        log = setup_logger("tests", replace_log_file=True)
        result = super().run(test)
        log.debug("Test results: " + str(result))
        return result