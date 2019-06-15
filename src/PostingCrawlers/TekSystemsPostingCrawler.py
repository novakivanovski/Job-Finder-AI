from .BasePostingCrawler import BasePostingCrawler
import json


class TekSystemsPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)
    
    def get_description(self):
        soup = self.posting.get_soup()
        attrs = {'type': 'application/ld+json'}
        json_text = soup.find('script', attrs=attrs).text
        raw = json.loads(json_text)['responsibilities']
        return raw
