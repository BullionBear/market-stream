import logging


def get_logger(name, level=logging.INFO):
    # Customizing the log format with a more accurate timestamp
    log_format = "[%(asctime)s.%(msecs)03d] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s"
    logging.basicConfig(level=level, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Creating a logger with the specified name
    logger = logging.getLogger(name)
    return logger
