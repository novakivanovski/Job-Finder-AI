from .BaseDescriptionCrawler import BaseDescriptionCrawler
from Utilities import ParsingUtilities
from Utilities import NetworkUtilities


class RecruitingInMotionDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)
    
    def get_description(self):
        job = self.job
        job_id = ParsingUtilities.get_value_between_strings(job.url, 'b=', '&')
        url = 'https://www2.pcrecruiter.net/pcrbin/jobboard.aspx?action=detail&b=' + job_id + \
              '&src=Indeed&utm_source=Indeed&utm_medium=organic&utm_campaign=Indeed&referrer=&referrer='
        response = NetworkUtilities.get_html(url, headers=self.headers)
        job.set_description(response.text)
        soup = job.get_soup()
        attrs = {'property': 'og:description'}
        meta = soup.find('meta', attrs=attrs)
        raw = meta['content']
        return raw

