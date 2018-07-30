import Tests.database_test
import Tests.resume_test
import Tests.stats_test
import Tests.system_test

run_test = {
  'Database': False,
  'Resume': True,
  'Stats': False,
  'System': False
}


test_entry_function = {
  'Database': Tests.database_test.run,
  'Resume': Tests.resume_test.run,
  'Stats': Tests.stats_test.run,
  'System': Tests.system_test.run
}


def get_tests_to_run():
    tests_to_run = []
    for test_name in run_test:
        if run_test[test_name]:
            tests_to_run.append(test_entry_function[test_name])

    return tests_to_run



