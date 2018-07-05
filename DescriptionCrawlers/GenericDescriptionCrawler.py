from . import BaseDescriptionCrawler


class GenericDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)

    def get_description(self):
        return self.generic_search()
