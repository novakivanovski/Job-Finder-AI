from importlib import import_module
from Utilities.ApplicationExceptions import loader_error


def load(package_name, class_name, *args, **kwargs):  # Use when class name is same as module
    return load_class(package_name, class_name, class_name, *args, **kwargs)


@loader_error()
def load_class(package_name, module_name, class_name, *args, **kwargs):
    full_module_name = package_name + '.' + module_name
    module_instance = import_module(full_module_name)
    class_pointer = getattr(module_instance, class_name)
    class_instance = class_pointer(*args, **kwargs)
    return class_instance

