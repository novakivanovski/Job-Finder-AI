import logging


class ApplicationException(Exception):
    pass


class NetworkError(ApplicationException):
    pass


class LoaderError(ApplicationException):
    pass


class ParsingError(ApplicationException):
    pass


class UnpackingError(ApplicationException):
    pass


class StatsError(ApplicationException):
    pass


class StorageError(ApplicationException):
    pass


class PostingCrawlerError(ApplicationException):
    pass


class CrawlerError(ApplicationException):
    pass


class PostingError(ApplicationException):
    pass


class ListingError(ApplicationException):
    pass


class ListerError(ApplicationException):
    pass


class MultiThreaderError(ApplicationException):
    pass


class DatabaseError(ApplicationException):
    pass


def network_error():
    return error(NetworkError)


def loader_error():
    return error(LoaderError)


def raise_crawler_error():
    return error(CrawlerError)


def error(reraise_error=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                process_exception(func, e, reraise_error)
        return wrapper
    return decorator


def pass_error():
    return error(reraise_error=None)


def process_exception(func, e, reraise_error):
    logging.error('Location of error: ' + func.__name__)
    logging.error('Error message: ' + str(e))
    if reraise_error:
        logging.error('Re-raising error: ' + reraise_error.__name__)
        raise reraise_error

