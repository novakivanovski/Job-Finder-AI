import NetworkUtilities
import logging
from .BaseDescriptionCrawler import BaseDescriptionCrawler


class AerotekDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)
    
    def get_description(self):
        self.headers['refresh'] = '0'
        soup = self.job.get_soup()
        job_text = ""
        for i in range(0, 2):
            try:
                text = soup.find('meta', attrs={'http-equiv': True})['content']
                start = text.find("'")
                end = text.find("'", start + 1)
                url = text[start + 1: end - 1]
                job_text = NetworkUtilities.get_html(url, headers=self.headers)
            except Exception as e:
                logging.error(e)
        self.job.set_description(job_text)
        soup = self.job.get_soup()
        raw = soup.get_text()
        return raw
