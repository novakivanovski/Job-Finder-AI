from . import BaseDescriptionCrawler


class IndeedDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init(job)

    def get_description(self):
        soup = self.job.get_soup()
        raw = soup.find(id="job_summary").get_text()
        return raw
