from Storage.config import tests_config
import logging
import os
from UI.CLI import CLI


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging_file = os.path.join('Tests', 'test_results.log')
    file_handle = logging.FileHandler(logging_file, 'w')
    file_handle.setLevel(logging.DEBUG)
    logger.addHandler(file_handle)
    logging.debug('------- START OF TEST -------\n')


def get_tests():
    return tests_config.get_tests_to_run()


if __name__ == '__main__':
    test_results = "ALL TESTS PASSED"
    setup_logger()
    tests_to_run = get_tests()
    try:
        for run_test_func in tests_to_run:
                run_test_func()
    except AssertionError:
        test_results = "TEST FAILURE"
    logging.info('Results: ' + test_results)
    print(test_results)

    interface = CLI()




