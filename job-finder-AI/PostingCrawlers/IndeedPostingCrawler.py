from .BasePostingCrawler import BasePostingCrawler


class IndeedPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        soup = self.posting.get_soup()
        raw = soup.find(class_="jobsearch-JobComponent-description icl-u-xs-mt--md").text
        return raw
