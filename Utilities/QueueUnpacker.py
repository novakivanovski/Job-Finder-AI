import logging
from bs4 import BeautifulSoup


def unpack(queue):
    items = []
    while not queue.empty():
        try:
            queue_item = queue.get()
            items.append(queue_item)
        except Exception as e:
            logging.error('Error unpacking queue: ' + str(e))
    return items


def unpack_to_soup(queue):
    html_texts = unpack(queue)
    soups = []
    try:
        for text in html_texts:
            soup = BeautifulSoup(text, 'html.parser')
            soups.append(soup)
    except Exception as e:
        logging.debug('Error unpacking to soup: ' + str(e))
    return soups


def unpack_metadata(metadata_queue):
    metadata_lists = unpack(metadata_queue)
    metadata = flatten_list(metadata_lists)
    return metadata


def flatten_list(lists):
    flattened_list = []
    for this_list in lists:
        for this_item in this_list:
            flattened_list.append(this_item)
    return flattened_list
