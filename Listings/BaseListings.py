from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class BaseListings(ABC):
    def __init__(self, listings_text, base_url=''):
        self.listings = listings_text
        self.base_url = base_url

    def get_metadata(self):
        metadata = []
        for listing_page in self.listings:
            page_metadata = self.get_page_metadata(listing_page)
            metadata += page_metadata
        return metadata

    @abstractmethod
    def get_page_metadata(self, listing):  # Override this
        pass

    @staticmethod
    def get_soup(text):
        soup = BeautifulSoup(text, 'html.parser')
        return soup
