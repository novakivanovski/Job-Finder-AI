from Tests import database_test
from Tests import system_test
import logging
import os


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging_file = os.path.join('Tests', 'test.log')
    fh = logging.FileHandler(logging_file, 'w')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logging.debug('Logger initialized.')


if __name__ == '__main__':
    run_system_test = False
    setup_logger()
    try:
        database_test.run()
        if run_system_test:
            system_test.run()
    except AssertionError as e:
        print(e)




