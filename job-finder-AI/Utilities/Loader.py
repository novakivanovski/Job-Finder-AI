from importlib import import_module
from Utilities.ApplicationExceptions import LoaderError


def load(package_name, class_name, *args, **kwargs):
    try:
        module_name = package_name + '.' + class_name
        module_instance = import_module(module_name)
        class_pointer = getattr(module_instance, class_name)
        class_instance = class_pointer(*args, **kwargs)
    except Exception as e:
        raise LoaderError('Loading error: ' + str(e))
    return class_instance






