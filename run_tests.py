from Tests import database_test
from Tests import system_test
from Tests import resume_test
from Tests import stats_test
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


def get_tests():
    tests = {system_test.run: False,
             database_test.run: False,
             resume_test.run: False,
             stats_test.run: True}
    return tests


if __name__ == '__main__':
    test_results = "ALL TESTS PASSED"
    setup_logger()
    run_test = get_tests()
    try:
        for test_function in run_test:
            if run_test[test_function]:
                test_function()
    except AssertionError:
        test_results = "TEST FAILURE"
    logging.info('Results: ' + test_results)




