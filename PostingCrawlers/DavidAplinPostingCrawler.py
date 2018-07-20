from .BasePostingCrawler import BasePostingCrawler
from Utilities import ParsingUtilities
from Utilities import NetworkUtilities
import json


class DavidAplinPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)
    
    def get_description(self):
        posting_url = self.posting.get_url()
        posting_id = ParsingUtilities.get_value_between_strings(posting_url, 'rpid=', '&')
        r = NetworkUtilities.get_html('https://api.aplin.com/postings/get-posting.json?posting_id=' + posting_id)
        json_txt = json.loads(r.text)['description']
        self.posting.set_text(json_txt)
        soup = self.posting.get_soup()
        raw = soup.get_text()
        return raw
