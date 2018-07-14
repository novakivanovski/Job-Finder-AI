import logging
from bs4 import BeautifulSoup


class QueueUnpacker:
    @staticmethod
    def unpack(queue):
        items = []
        while not queue.empty():
            try:
                queue_item = queue.get()
                items.append(queue_item)
            except Exception as e:
                logging.error('Error unpacking queue: ' + str(e))
        return items

    @staticmethod
    def unpack_to_soup(queue):
        html_texts = QueueUnpacker.unpack(queue)
        soups = []
        try:
            for text in html_texts:
                soup = BeautifulSoup(text, 'html.parser')
                soups.append(soup)
        except Exception as e:
            logging.debug('Error unpacking to soup: ' + str(e))
        return soups


    @staticmethod
    def unpack_metadata(metadata_queue):
        metadata_lists = QueueUnpacker.unpack(metadata_queue)
        metadata = QueueUnpacker.flatten_list(metadata_lists)
        return metadata

    @staticmethod
    def flatten_list(lists):
        flattened_list = []
        for this_list in lists:
            for this_item in this_list:
                flattened_list.append(this_item)
        return flattened_list
