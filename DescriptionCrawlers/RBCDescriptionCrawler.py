from . import BaseDescriptionCrawler
import json


class RBCDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)
        
    def get_description(self):
        soup = self.job.get_soup()
        attrs = {'type': 'text/javascript'}
        raw = soup.find('script', attrs=attrs).get_text()
        start = raw.find('{"status":200')
        end = raw.find(',"flashParams', start)
        json_data = json.loads(raw[start:end])
        job_text = json_data['data']['job']['description']
        self.job.set_description(job_text)
        soup = self.job.get_soup()
        raw = soup.get_text()
        return raw
