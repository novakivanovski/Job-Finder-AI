from .BasePostingCrawler import BasePostingCrawler


class TalgroupPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)
    
    def get_description(self):
        soup = self.posting.get_soup()
        raw = soup.get_text()
        return raw
