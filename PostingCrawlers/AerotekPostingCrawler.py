from Utilities import NetworkUtilities
import logging
from .BasePostingCrawler import BasePostingCrawler


class AerotekPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)
    
    def get_description(self):
        self.headers['refresh'] = '0'
        soup = self.posting.get_soup()
        page = None
        for i in range(0, 2):
            try:
                text = soup.find('meta', attrs={'http-equiv': True})['content']
                start = text.find("'")
                end = text.find("'", start + 1)
                url = text[start + 1: end - 1]
                page = NetworkUtilities.get_page(url, headers=self.headers)
            except Exception as e:
                logging.error(e)
        self.posting.update_page(page)
        soup = self.posting.get_soup()
        raw = soup.get_text()
        return raw
