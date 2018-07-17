from abc import ABC, abstractmethod


class BaseParser(ABC):
    def __init__(self, base_url):
        self.base_url = base_url

    def get_metadata(self, page_soups):
        metadata = []
        for soup in page_soups:
            page_metadata = self.get_page_metadata_from_soup(soup)
            metadata += page_metadata
        return metadata

    @abstractmethod
    def get_page_metadata_from_soup(self, page_soup):  # Override this
        pass
