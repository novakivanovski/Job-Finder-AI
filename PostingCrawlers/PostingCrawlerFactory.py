from Utilities import Loader
import logging


class PostingCrawlerFactory:
    def __init__(self):
        self.indeed = 'ca.indeed.com'
        self.crawlers = {'IndeedPostingCrawler': 'ca.indeed.com',
                         'TalgroupPostingCrawler': 'talgroup.net',
                         'WorkdayPostingCrawler': 'myworkdaypostings.com',
                         'AerotekPostingCrawler': 'www.aplitrak.com',
                         'GenericPostingCrawler': ''}
        self.package_name = 'PostingCrawlers'

    def get(self, posting):
        crawler_instance = None
        try:
            url = posting.get_url()
            for crawler_class in self.crawlers:
                posting_site = self.crawlers[crawler_class]
                if self.is_match(url, posting_site):
                    logging.debug('Match found: ' + url + ' with ' + posting_site)
                    crawler_instance = Loader.load(self.package_name, crawler_class, posting)
        except Exception as e:
            logging.error('Unable to retrieve a crawler instance: ' + str(e))
            raise
        return crawler_instance

    @staticmethod
    def is_match(url, posting_site):
        if not url:
            raise ValueError('No url exists in posting description')
        return url.find(posting_site) != -1


'''''
        indeed = posting.url.find('ca.indeed.com') != -1
        talgroup = posting.url.find('talgroup.net') != -1
        workday = posting.url.find('myworkdaypostings.com') != -1
        aerotek = posting.url.find('www.aplitrak.com') != -1
        smoothhiring = posting.url.find('app.smoothhiring.com') != -1
        rbc = posting.url.find('postings.rbc.com') != -1
        brassring = posting.url.find('krb-spostings.brassring.com') != -1
        eagle = posting.url.find('postings.eagleonline.com') != -1
        taleo = posting.url.find('taleo.net') != -1
        david_aplin = posting.url.find('www.aplin.com') != -1
        adp = posting.url.find('workforcenow.adp.com') != -1
        postingdiva = posting.url.find('postingdiva.com') != -1
        recruitinginmotion = posting.url.find('recruitinginmotion.com') != -1
        webconnect = posting.url.find('webconnect.sendouts.net') != -1
        akamai = posting.company.find('Akamai') != -1
        ian_martin = posting.url.find('careers.ianmartin.com') != -1
        teksystems = posting.url.find('www.teksystems.com') != -1
        hire_google = posting.url.find('hire.withgoogle.com') != -1
        google = posting.url.find('careers.google.com') != -1
'''''
