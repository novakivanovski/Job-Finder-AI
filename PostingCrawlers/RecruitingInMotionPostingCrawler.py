from .BasePostingCrawler import BasePostingCrawler
from Utilities import ParsingUtilities
from Utilities import NetworkUtilities


class RecruitingInMotionPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)
    
    def get_description(self):
        posting = self.posting
        posting_id = ParsingUtilities.get_value_between_strings(posting.url, 'b=', '&')
        url = 'https://www2.pcrecruiter.net/pcrbin/postingboard.aspx?action=detail&b=' + posting_id + \
              '&src=Indeed&utm_source=Indeed&utm_medium=organic&utm_campaign=Indeed&referrer=&referrer='
        response = NetworkUtilities.get_html(url, headers=self.headers)
        posting.set_text(response.text)
        soup = posting.get_soup()
        attrs = {'property': 'og:description'}
        meta = soup.find('meta', attrs=attrs)
        raw = meta['content']
        return raw

