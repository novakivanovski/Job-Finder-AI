from cryptography.fernet import Fernet
from Storage.LocalStorage import LocalStorage


class Security:
    def __init__(self):
        key = self.get_key()
        self.cipher_suite = Fernet(key)

    @staticmethod
    def get_key():
        key = LocalStorage.get_key()
        if not key:
            key = Fernet.generate_key()
        return key

    def encrypt(self, data):
        encrypted_data = self.cipher_suite.encrypt(data)
        return encrypted_data

    def decrypt(self, cipher_data):
        plain_text = self.cipher_suite.decrypt(cipher_data)
        return plain_text



