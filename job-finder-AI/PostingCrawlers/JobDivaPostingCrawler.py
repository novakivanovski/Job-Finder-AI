from .BasePostingCrawler import BasePostingCrawler


class JobDivaPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)
    
    def get_description(self):
        soup = self.posting.get_soup()
        raw = soup.find(class_='posting_des').get_text()
        return raw

