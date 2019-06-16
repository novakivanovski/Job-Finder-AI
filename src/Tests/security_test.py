import os
import pytest


@pytest.fixture
def security_instance():
    from Utilities.Security import Security
    return Security()


def test_key(security_instance):
    key = security_instance.get_key()
    assert len(key) >= 32


def test_cipher(security_instance):
    test_file_path = os.path.join('Storage', 'LocalStorage.py')
    with open(test_file_path, 'rb') as test_file:
        expected_data = test_file.read()
    encrypted_data = security_instance.encrypt(expected_data)
    actual_data = security_instance.decrypt(encrypted_data)
    assert actual_data == expected_data

