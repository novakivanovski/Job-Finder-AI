from .BaseDescriptionCrawler import BaseDescriptionCrawler
from Utilities import NetworkUtilities
import logging


class EagleDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)

    def get_description(self):
        job_text = ''
        try:
            url = self.job.get_entry_url()
            response = NetworkUtilities.get_html(url, headers=self.headers)
            job_text = response.text
        except Exception as e:
            logging.error(e)
        self.job.set_description(job_text)
        return self.generic_search()
