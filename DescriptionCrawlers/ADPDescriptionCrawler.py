from .BaseDescriptionCrawler import BaseDescriptionCrawler
from JobParser import JobParser
import requests
import json


class ADPDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)
    
    def get_description(self):
        job = self.job
        job_id = JobParser.get_value_between_strings(job.url, 'jobId=', '&')
        client = JobParser.get_value_between_strings(job.url, 'client=', '&')
        first_url = 'https://workforcenow.adp.com/jobs/apply/common/careercenter.faces?client=' + client + \
                    '&op=0&locale=en_US&mode=LIVE&access=E&jobId=' + job_id + '6&source=IN&A=N&dojo.preventCache=0'
        second_url = 'https://workforcenow.adp.com/jobs/apply/metaservices/careerCenter/jobDetails/E/en_US?' + \
                     'requisitionOid=' + job_id + '&ccRefId=19000101&client=' + client
        s = requests.Session()
        s.get(first_url)
        r = s.get(second_url)
        text = json.loads(r.text)['data']['description']
        job.set_description(text)
        soup = job.get_soup()
        return soup.get_text()
