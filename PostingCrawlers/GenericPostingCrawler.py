from .BasePostingCrawler import BasePostingCrawler


class GenericPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        return self.generic_search()
