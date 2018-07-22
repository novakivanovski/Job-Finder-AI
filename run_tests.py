from Tests import database_test
from Tests import system_test
import logging


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('test.log', 'w')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logging.debug('Logger initialized.')


if __name__ == '__main__':
    run_system_test = False
    setup_logger()
    database_test.run()
    if run_system_test:
        system_test.run()




