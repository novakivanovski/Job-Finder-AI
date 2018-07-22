from abc import ABC, abstractmethod


class BaseLister(ABC):
    def __init__(self, base_url):
        self.pages = []
        self.base_url = base_url
        self.job_id = 0

    def get_job_id(self):
        self.job_id += 1
        return self.job_id

    def add_pages(self, pages):
        for page in pages:
            self.add_page(page)

    def add_page(self, page):
        self.pages.append(page)

    def get_listings(self):
        total_listings = []
        for page in self.pages:
            page_listings = self.get_listings_from_page(page)
            total_listings += page_listings
        return total_listings

    @abstractmethod
    def get_listings_from_page(self, page):  # Override this
        pass

