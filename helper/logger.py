import logging


def get_logger(name):
    # Customizing the log format with a more accurate timestamp
    log_format = "[%(asctime)s.%(msecs)03d] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Creating a logger with the specified name
    logger = logging.getLogger(name)
    return logger
