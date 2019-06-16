from Utilities.Security import Security
import os
from Tests import TestingTools


@TestingTools.timer
def test_run():
    security = Security()
    test_file_path = os.path.join('Storage', 'LocalStorage.py')
    with open(test_file_path, 'rb') as test_file:
        expected_data = test_file.read()
    encrypted_data = security.encrypt(expected_data)
    actual_data = security.decrypt(encrypted_data)
    TestingTools.assert_equal(actual_data, expected_data)

