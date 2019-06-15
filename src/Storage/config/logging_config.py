import logging
import os

logger = None


def setup_logger(logger_name):
    logger_path = os.path.join('Storage', 'logs', logger_name)
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handle = logging.FileHandler(logger_path, 'w')
    file_handle.setLevel(logging.DEBUG)
    logger.addHandler(file_handle)
    logging.debug('------- Logger initialized. -------\n')
    return logger


def get_logger():
    return logger


