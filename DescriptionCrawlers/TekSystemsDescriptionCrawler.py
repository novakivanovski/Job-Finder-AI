from .BaseDescriptionCrawler import BaseDescriptionCrawler
import json


class TekSystemsDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)
    
    def get_description(self):
        soup = self.job.get_soup()
        attrs = {'type': 'application/ld+json'}
        json_text = soup.find('script', attrs=attrs).text
        raw = json.loads(json_text)['responsibilities']
        return raw
