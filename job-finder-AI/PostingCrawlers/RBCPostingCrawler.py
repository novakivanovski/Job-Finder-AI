from .BasePostingCrawler import BasePostingCrawler
import json
from bs4 import BeautifulSoup


class RBCPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)
        
    def get_description(self):
        soup = self.posting.get_soup()
        attrs = {'type': 'text/javascript'}
        raw = soup.find('script', attrs=attrs).get_text()
        start = raw.find('{"status":200')
        end = raw.find(',"flashParams', start)
        json_data = json.loads(raw[start:end])
        posting_text = json_data['data']['posting']['description']
        soup = BeautifulSoup(posting_text, 'html.parser')
        raw = soup.get_text()
        return raw
