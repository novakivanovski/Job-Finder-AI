from .BasePostingCrawler import BasePostingCrawler
from Utilities import NetworkUtilities
from Utilities.ParseUtility import ParseUtility
import json


class IanMartinPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        url = self.posting.get_url()
        posting_id = ParseUtility.get_value_between_strings(url, '/postings/', '?')
        base_url = 'https://public-rest33.bullhornstaffing.com/rest-services/16XNKG/query/postingBoardPost?'
        url = base_url + 'start=0&count=1&where=id=' + posting_id +\
            '&fields=id,title,publishedCategory(id,name),address(city,state),employmentType,' \
            'dateLastPublished,publicDescription,isOpen,isPublic,isDeleted'
        page = NetworkUtilities.get_page(url)
        text = json.loads(page.text)['data'][0]['publicDescription']
        page.text = text
        self.posting.set_page(page)
        raw = self.posting.get_soup().text
        return raw
