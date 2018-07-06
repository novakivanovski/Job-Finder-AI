from . import BaseDescriptionCrawler
import NetworkUtilities
from JobParser import JobParser
import json


class IanMartinDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)

    def get_description(self):
        url = self.job.get_entry_url()
        job_id = JobParser.get_value_between_strings(url, '/jobs/', '?')
        url = 'https://public-rest33.bullhornstaffing.com/rest-services/16XNKG/query/JobBoardPost?start=0&count=1&' \
              'where=id=' + job_id + '&fields=id,title,publishedCategory(id,name),address(city,state),employmentType,' \
              'dateLastPublished,publicDescription,isOpen,isPublic,isDeleted'
        response = NetworkUtilities.get_html(url)
        text = json.loads(response.text)['data'][0]['publicDescription']
        self.job.set_description(text)
        raw = self.job.get_soup().text
        return raw