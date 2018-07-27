from bs4 import BeautifulSoup
from Utilities.ApplicationExceptions import UnpackingError


def unpack(queue):
    items = []
    while not queue.empty():
        try:
            queue_item = queue.get()
            if queue_item:
                items.append(queue_item)
        except Exception:
            raise UnpackingError('Error unpacking queue')
    return items


def unpack_to_soup(queue):
    html_texts = unpack(queue)
    soups = []
    try:
        for text in html_texts:
            soup = BeautifulSoup(text, 'html.parser')
            soups.append(soup)
    except Exception:
        raise UnpackingError('Error unpacking queue to soup')
    return soups


def flatten_list(lists):
    flattened_list = []
    try:
        for this_list in lists:
            for this_item in this_list:
                flattened_list.append(this_item)
    except Exception:
        raise UnpackingError('Error flattening list')
    return flattened_list
