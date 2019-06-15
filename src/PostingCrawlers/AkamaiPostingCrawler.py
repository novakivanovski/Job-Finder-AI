from .BasePostingCrawler import BasePostingCrawler
from Utilities import Network


class AkamaiPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        raw = ''
        link = self.posting.get_url()
        for i in range(4):
            response = Network.get_html(link, allow_redirects=False)
            link = response.headers['Location']
        page = Network.get_page(link)
        self.posting.set_page(page)
        soup = self.posting.get_soup()
        tags = soup.find_all('p', style="margin-top:0px;margin-bottom:0px")
        for tag in tags:
            raw += tag.text + '\n'
        return raw
