from .BaseDescriptionCrawler import BaseDescriptionCrawler


class TalgroupDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)
    
    def get_description(self):
        soup = self.job.get_soup()
        raw = soup.get_text()
        return raw
