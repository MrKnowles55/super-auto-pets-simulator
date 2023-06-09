import logging


class CustomFormatter(logging.Formatter):
    def format(self, record):
        module_name = record.name.split('.')[-1]  # get the last part after the dot
        record.name = module_name
        return super().format(record)


def setup_logging(level):
    # Create a formatter
    formatter = CustomFormatter('%(name)7s - %(levelname)7s - %(message)s')

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    # Add the console handler to the root logger
    logging.getLogger().addHandler(ch)

    # Set the root logger level
    logging.getLogger().setLevel(level)


def get_custom_logger(name):
    logger = logging.getLogger(name)
    return logger

