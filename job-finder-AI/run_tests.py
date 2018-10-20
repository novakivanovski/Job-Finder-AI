from Storage.config import tests_config, logging_config
from UI.CLI import CLI


if __name__ == '__main__':
    test_results = "ALL TESTS PASSED"
    logger = logging_config.setup_logger('test_results.log')
    tests_to_run = tests_config.get_tests_to_run()
    try:
        for run_test_func in tests_to_run:
            run_test_func()
    except AssertionError:
        test_results = "TEST FAILURE"
    logger.info('Results: ' + test_results)
    print(test_results)




