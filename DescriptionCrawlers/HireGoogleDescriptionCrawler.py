from . import BaseDescriptionCrawler


class GoogleDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)

    def get_description(self):
        soup = self.job.get_soup()
        job_posting_content = soup.find(class_='bb-jobs-posting__content')
        raw = job_posting_content.text
        return raw
