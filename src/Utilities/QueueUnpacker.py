from bs4 import BeautifulSoup
from Utilities.ApplicationExceptions import unpack_error


@unpack_error()
def unpack(queue):
    items = []
    while not queue.empty():
        queue_item = queue.get()
        if queue_item:
                items.append(queue_item)
    return items


def unpack_to_soup(queue):
    html_texts = unpack(queue)
    soups = []
    for text in html_texts:
            soup = BeautifulSoup(text, 'html.parser')
            soups.append(soup)
    return soups


@unpack_error()
def flatten_list(lists):
    flattened_list = []
    for sublist in lists:
        for item in sublist:
            flattened_list.append(item)
    return flattened_list
