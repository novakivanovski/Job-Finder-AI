import Tests.database_test
import Tests.resume_test
import Tests.stats_test
import Tests.system_test
import Tests.gui_test
import Tests.security_test
import Tests.sandbox_test

test_name_to_entry_function = {
  'Database': Tests.database_test.run,
  'Resume': Tests.resume_test.run,
  'Stats': Tests.stats_test.run,
  'System': Tests.system_test.run,
  'GUI': Tests.gui_test.run,
  'Security': Tests.security_test.run,
  'Sandbox': Tests.sandbox_test.run
}


def get_test_function(test_name):
    if test_name not in test_name_to_entry_function:
        raise KeyError('Invalid test specified: ' + test_name)
    return test_name_to_entry_function[test_name]




