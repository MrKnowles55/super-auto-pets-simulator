import logging
import os
from config_utils.config import config_handler
from logging.handlers import RotatingFileHandler

DEBUG_MODE = config_handler.config_data['DEBUG_MODE']

# Get the path of the logger.py script
logger_script_path = os.path.abspath(__file__)
# Get the parent directory of the logger.py script (i.e., the 'src' directory)
parent_dir = os.path.dirname(os.path.dirname(logger_script_path))

# Set the log file path relative to the 'src' directory
log_path = os.path.join(parent_dir, r"../data/logs/debug.log")

MODULE_FILTER = config_handler.config_data.get('DEBUG_FILTER', [])


class ModuleFilter(logging.Filter):
    def __init__(self, module_filter):
        super().__init__()
        self.module_filter = module_filter

    def filter(self, record):
        if not self.module_filter:
            return True
        return record.name in self.module_filter


if DEBUG_MODE:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.WARNING


def delete_log_file(log_file, replace_log_file):
    if os.path.isfile(log_file) and replace_log_file:
        with open(log_file, 'w') as file:
            file.truncate(0)


def setup_logger(name, log_level=LOG_LEVEL, log_file=log_path, replace_log_file=False):
    name = name.replace("src.", "")
    logger = logging.getLogger(name)
    delete_log_file(log_file, replace_log_file)
    logger.setLevel(log_level)

    # Check if logger already has handlers, if yes then return the existing logger
    if logger.hasHandlers():
        return logger
    # Create a file handler for writing log messages to the specified file
    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    file_handler.setLevel(log_level)

    # Create a log formatter and set it for the file handler
    # formatter = logging.Formatter('%(asctime)s - %(name)-30s - %(levelname)-8s - %(message)s')
    formatter = logging.Formatter('%(name)-30s - %(message)s')
    file_handler.setFormatter(formatter)

    # Remove all existing handlers (including the default StreamHandler)
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Add the custom filter to the logger
    module_filter = ModuleFilter(MODULE_FILTER)
    logger.addFilter(module_filter)

    logger.propagate = False

    return logger

