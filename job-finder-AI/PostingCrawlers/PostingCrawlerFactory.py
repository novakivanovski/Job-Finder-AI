from Utilities import Loader
import logging
from PostingCrawlers.config import mapping


class PostingCrawlerFactory:
    def __init__(self):
        self.indeed = 'ca.indeed.com'
        self.crawlers = mapping.crawler_map
        self.package_name = 'PostingCrawlers'

    def get(self, job):
        crawler_instance = None
        try:
            url = job.get_posting_url()
            for crawler_class in self.crawlers:
                posting_site = self.crawlers[crawler_class]
                if self.is_match(url, posting_site):
                    logging.debug('Match found: ' + url + ' with ' + posting_site)
                    crawler_instance = Loader.load(self.package_name, crawler_class, job.posting)
        except Exception as e:
            logging.error('Unable to retrieve a crawler instance: ' + str(e))
            raise e
        return crawler_instance

    @staticmethod
    def is_match(url, posting_site):
        if not url:
            raise ValueError('No url exists in posting description')
        return url.find(posting_site) != -1
