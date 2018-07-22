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
    setup_logger()
    system_test.run()




