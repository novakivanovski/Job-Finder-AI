from .BasePostingCrawler import BasePostingCrawler


class IndeedPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        raw = 'Indeed placeholder text'
        soup = self.posting.get_soup()
        if soup:
            raw = soup.find(id="posting_summary").get_text()
        return raw
