import logging


class CustomFormatter(logging.Formatter):
    def format(self, record):
        module_name = record.name.split('.')[-1]  # get the last part after the dot
        function_name = record.funcName
        record.name = f"{function_name}.{module_name.upper()}"
        return super().format(record)


def setup_logging(level):
    # Create a formatter
    formatter = CustomFormatter('%(levelname)7s - %(name)25s - %(message)s')

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

