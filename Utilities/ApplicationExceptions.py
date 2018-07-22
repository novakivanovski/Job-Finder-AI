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


