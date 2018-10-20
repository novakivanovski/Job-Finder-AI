from Storage.LocalStorage import LocalStorage


def run():
    storage = LocalStorage()
    storage.create_backup()