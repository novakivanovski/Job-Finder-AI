from .BasePostingCrawler import BasePostingCrawler


class GooglePostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        soup = self.posting.get_soup()
        posting_posting_content = soup.find(class_='bb-postings-posting__content')
        raw = posting_posting_content.text
        return raw
