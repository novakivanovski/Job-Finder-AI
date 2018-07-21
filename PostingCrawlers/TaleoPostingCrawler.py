from .BasePostingCrawler import BasePostingCrawler


class TaleoPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        posting_text = self.posting.get_text()
        search_string = "'descRequisition', "
        start = posting_text.find(search_string)
        if start != -1:  # taleo api
            start = start + len(search_string)
            end = posting_text.find(']', start) + 1
            raw = posting_text[start:end]
        else:
            raw = self.generic_search()
        return raw
