import logging
import os
from config import config_handler
from logging.handlers import RotatingFileHandler

DEBUG_MODE = config_handler.config_data['DEBUG_MODE']

# Get the path of the logger.py script
logger_script_path = os.path.abspath(__file__)
# Get the parent directory of the logger.py script (i.e., the 'src' directory)
parent_dir = os.path.dirname(os.path.dirname(logger_script_path))

# Set the log file path relative to the 'src' directory
log_path = os.path.join(parent_dir, r"data\logs\debug.log")

if DEBUG_MODE:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.WARNING


def setup_logger(name, log_level=LOG_LEVEL, log_file=log_path):
    print(name, DEBUG_MODE, log_file)
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Check if logger already has handlers, if yes then return the existing logger
    if logger.hasHandlers():
        return logger
    # Create a file handler for writing log messages to the specified file
    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    file_handler.setLevel(log_level)

    # Create a log formatter and set it for the file handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Remove all existing handlers (including the default StreamHandler)
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger
