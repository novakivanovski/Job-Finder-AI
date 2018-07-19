from importlib import import_module
import logging


def get(text, listing_type):
    try:
        class_name = listing_type
        module_name = 'Listings' + '.' + class_name
        listings_module = import_module(module_name)
        listings_class = getattr(listings_module, class_name)
        listings_instance = listings_class(text)
    except Exception as e:
        logging.error('Unable to retrieve a crawler instance: ' + str(e))
        raise
    return listings_instance
