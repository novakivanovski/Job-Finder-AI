import NetworkUtilities
from .BaseDescriptionCrawler import BaseDescriptionCrawler


class WorkdayDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)
    
    def get_description(self):
        self.headers['Accept'] = 'application/json,application/xml'
        url = self.job.get_entry_url()
        response = NetworkUtilities.get_html(url, headers=self.headers)
        self.job.set_description(response.text)
        soup = self.job.get_soup()
        raw = soup.get_text()
        return raw
