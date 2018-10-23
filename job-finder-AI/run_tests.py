from Storage.config import logging_config
from Tests import tests_config

tests_to_enable = {
    'Database': False,
    'Resume': False,
    'Stats': False,
    'System': True,
    'GUI': False,
    'Security': False,
    'Sandbox': False
}


def get_test_run_functions():
    run_functions = []
    for test_name in tests_to_enable:
        test_enabled = tests_to_enable[test_name]
        if test_enabled:
            test_function = tests_config.get_test_function(test_name)
            run_functions.append(test_function)
    return run_functions


if __name__ == '__main__':
    logger = logging_config.setup_logger('test_results.log')
    test_run_functions = get_test_run_functions()
    test_result = "TEST SUCCESS"
    try:
        for test_run_function in test_run_functions:
            logger.info('Running test: ' + test_run_function.__module__)
            test_run_function()
    except AssertionError:
        test_result = "TEST FAILURE"
    logger.info(test_result)
    print(test_result)




