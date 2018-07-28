from .BasePostingCrawler import BasePostingCrawler
from Utilities.ParseUtility import ParseUtility
from Utilities import NetworkUtilities
import json
from bs4 import BeautifulSoup


class DavidAplinPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)
    
    def get_description(self):
        posting_url = self.posting.get_url()
        posting_id = ParseUtility.get_value_between_strings(posting_url, 'rpid=', '&')
        page = NetworkUtilities.get_page('https://api.aplin.com/postings/get-posting.json?posting_id=' + posting_id)
        self.posting.set_page(page)
        json_txt = json.loads(page.text)['description']
        soup = BeautifulSoup(json_txt, 'html.parser')
        raw = soup.get_text()
        return raw
