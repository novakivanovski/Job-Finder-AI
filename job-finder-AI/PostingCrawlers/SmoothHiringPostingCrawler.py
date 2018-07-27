from .BasePostingCrawler import BasePostingCrawler


class SmoothHiringPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)
        
    def get_description(self):
        soup = self.posting.get_soup()
        script_tags = soup.find_all('script')
        start = script_tags[10].text.find('{"id"')
        end = script_tags[10].text.find('};')
        raw = script_tags[10].text[start:end+1]
        return raw

