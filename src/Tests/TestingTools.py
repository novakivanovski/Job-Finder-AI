from DataStructures.Job import Job
from DataStructures.Listing import Listing
from DataStructures.Posting import Posting
from DataStructures.Page import Page
from Storage import LocalStorage
import logging
import os
import time


def assert_equal(actual, expected):
    result = actual == expected
    assert_fmt = "{} == {} ? {}"
    assert_string = assert_fmt.format(actual, expected, result)
    logging.debug(assert_string)
    if not result:
        raise AssertionError


def assert_approx(actual, expected):
    float_tolerance = 1e-6
    difference = abs(actual - expected)
    assert_equal(difference < float_tolerance, True)


def get_test_job():
    test_posting = get_test_posting()
    test_job = Job(test_posting)
    return test_job


def get_test_posting():
    test_listing = get_test_listing()
    test_page = get_test_page()
    test_posting = Posting(test_listing, test_page)
    return test_posting


def get_test_listing():
    test_listing = Listing()
    return test_listing


def get_test_page():
    test_page = Page('', '')
    return test_page


def set_job_parameters(job, job_id=0, title='', date='', company='', location='', plaintext=''):
    job.set_id(job_id)
    job.listing.title = title
    job.listing.date = date
    job.listing.company = company
    job.listing.location = location
    job.set_plaintext(plaintext)


def debug(func):
    def wrapper(*args, **kwargs):
        logging.debug('=' * 25)
        logging.debug('Enter function ' + func.__name__)
        logging.debug('Positional arguments: ' + str(args))
        logging.debug('Keyword arguments: ' + str(kwargs))
        func(*args, **kwargs)
        logging.debug('Exit function ' + func.__name__)
        logging.debug('=' * 25 + '\n')
    return wrapper


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        elapsed = int(end-start)
        print('{} elapsed run time: {}s'.format(func.__module__, elapsed))
    return wrapper


@debug
def delete_db():
    database_path = os.path.join('Storage', 'config', 'database.db')
    if os.path.isfile(database_path):
        os.unlink(database_path)


def reset_db():
    delete_db()
    storage = LocalStorage.LocalStorage()
    return storage.database
