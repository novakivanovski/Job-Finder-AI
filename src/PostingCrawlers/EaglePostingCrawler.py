from .BasePostingCrawler import BasePostingCrawler
from Utilities import Network
import logging


class EaglePostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        page = None
        try:
            url = self.posting.get_url()
            page = Network.get_page(url, headers=self.headers)
        except Exception as e:
            logging.error(e)
        self.posting.set_page(page)
        return self.generic_search()
