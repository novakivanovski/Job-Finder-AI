from .BasePostingCrawler import BasePostingCrawler
import json


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
        self.posting.set_text(posting_text)
        soup = self.posting.get_soup()
        raw = soup.get_text()
        return raw
