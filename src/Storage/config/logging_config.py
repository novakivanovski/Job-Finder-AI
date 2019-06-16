import logging
import os

logger = None


def setup_logger(logger_name):
    logs_folder = os.path.join('Storage', logs')
    logger_path = os.path.join(logs_folder, logger_name)
    
    if not os.path.isdir(logs_folder):
        os.mkdirs(logs_folder)
                             
    with open(logger_path, 'w') as log_file:
        pass
    
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


