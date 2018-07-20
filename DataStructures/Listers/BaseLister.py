from abc import ABC, abstractmethod


class BaseLister(ABC):
    def __init__(self, pages, base_url=''):
        self.pages = pages
        self.base_url = base_url
        self.listings = self.get_listings()

    def get_listings(self):
        total_listings = []
        for page in self.pages:
            page_listings = self.get_listing_from_page(page)
            total_listings += page_listings
        return total_listings

    @abstractmethod
    def get_listing_from_page(self, page):  # Override this
        pass

