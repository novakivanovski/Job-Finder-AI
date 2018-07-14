from .BaseDescriptionCrawler import BaseDescriptionCrawler
from JobParser import JobParser
import NetworkUtilities
import json


class DavidAplinDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)
    
    def get_description(self):
        job_url = self.job.get_entry_url()
        job_id = JobParser.get_value_between_strings(job_url, 'rpid=', '&')
        r = NetworkUtilities.get_html('https://api.aplin.com/jobs/get-job.json?job_id=' + job_id)
        json_txt = json.loads(r.text)['description']
        self.job.set_description(json_txt)
        soup = self.job.get_soup()
        raw = soup.get_text()
        return raw
