from Utilities import NetworkUtilities
from .BasePostingCrawler import BasePostingCrawler


class WorkdayPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)
    
    def get_description(self):
        self.headers['Accept'] = 'application/json,application/xml'
        url = self.posting.get_url()
        response = NetworkUtilities.get_html(url, headers=self.headers)
        self.posting.set_text(response.text)
        soup = self.posting.get_soup()
        raw = soup.get_text()
        return raw
