from .BaseDescriptionCrawler import BaseDescriptionCrawler


class IndeedDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)

    def get_description(self):
        raw = 'Indeed placeholder text'
        soup = self.job.get_soup()
        if soup:
            raw = soup.find(id="job_summary").get_text()
        return raw
