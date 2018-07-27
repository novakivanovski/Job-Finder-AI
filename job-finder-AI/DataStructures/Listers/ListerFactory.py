from Utilities import Loader


def get(listings, class_name):
    package_name = 'DataStructures.Listers'
    listings_instance = Loader.load(package_name, class_name, listings)
    return listings_instance
