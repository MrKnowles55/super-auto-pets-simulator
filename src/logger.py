import logging
import os
from config import config_handler
from logging.handlers import RotatingFileHandler

DEBUG_MODE = config_handler.config_data['DEBUG_MODE']

parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
log_path = os.path.join(parent_dir, "data/logs/debug.log")

if DEBUG_MODE:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.WARNING


def setup_logger(name, log_level=logging.DEBUG, log_file=log_path):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # If log_file is specified, log messages to the file
    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
