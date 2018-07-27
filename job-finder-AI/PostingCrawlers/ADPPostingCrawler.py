from .BasePostingCrawler import BasePostingCrawler
import requests
import json
from Utilities import ParsingUtilities
from DataStructures.Page import Page


class ADPPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)
    
    def get_description(self):
        posting = self.posting
        posting_url = posting.get_url()
        posting_id = ParsingUtilities.get_value_between_strings(posting_url, 'postingId=', '&')
        client = ParsingUtilities.get_value_between_strings(posting_url, 'client=', '&')
        first_url = 'https://workforcenow.adp.com/postings/apply/common/careercenter.faces?client=' + client + \
                    '&op=0&locale=en_US&mode=LIVE&access=E&postingId=' + posting_id + \
                    '6&source=IN&A=N&dojo.preventCache=0'
        second_url = 'https://workforcenow.adp.com/postings/apply/metaservices/careerCenter/postingDetails/E/en_US?' + \
                     'requisitionOid=' + posting_id + '&ccRefId=19000101&client=' + client
        s = requests.Session()
        s.get(first_url)
        r = s.get(second_url)
        text = json.loads(r.text)['data']['description']
        page = Page(text, r.url)
        posting.set_page(page)
        soup = posting.get_soup()
        return soup.get_text()
