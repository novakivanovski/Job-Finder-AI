from .BaseDescriptionCrawler import BaseDescriptionCrawler


class WebConnectDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)

    def get_description(self):
        soup = self.job.get_soup()
        span = soup.find('span', id='lblDescription')
        return span.text
