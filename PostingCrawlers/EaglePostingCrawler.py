from .BasePostingCrawler import BasePostingCrawler
from Utilities import NetworkUtilities
import logging


class EaglePostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        posting_text = ''
        try:
            url = self.posting.get_url()
            response = NetworkUtilities.get_html(url, headers=self.headers)
            posting_text = response.text
        except Exception as e:
            logging.error(e)
        self.posting.set_text(posting_text)
        return self.generic_search()
