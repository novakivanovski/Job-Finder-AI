import logging
import os


def setup_logger(logger_name):
    logger_path = os.path.join('Storage', 'logs', logger_name)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handle = logging.FileHandler(logger_path, 'w')
    file_handle.setLevel(logging.DEBUG)
    logger.addHandler(file_handle)
    logging.debug('------- Logger initialized. -------\n')
    return logger

