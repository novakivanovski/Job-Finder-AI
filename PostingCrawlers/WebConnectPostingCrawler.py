from .BasePostingCrawler import BasePostingCrawler


class WebConnectPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        soup = self.posting.get_soup()
        span = soup.find('span', id='lblDescription')
        return span.text

