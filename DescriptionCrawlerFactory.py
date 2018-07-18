from importlib import import_module
import logging


class DescriptionCrawlerFactory:
    def __init__(self):
        self.indeed = 'ca.indeed.com'
        self.crawlers = {'IndeedDescriptionCrawler': 'ca.indeed.com',
                         'TalgroupDescriptionCrawler': 'talgroup.net',
                         'WorkdayDescriptionCrawler': 'myworkdayjobs.com',
                         'AerotekDescriptionCrawler': 'www.aplitrak.com',
                         'GenericDescriptionCrawler': ''}
        self.package_name = 'DescriptionCrawlers'

    def get(self, job):
        crawler_instance = None
        try:
            url = job.get_url()
            for crawler_type in self.crawlers:
                job_site = self.crawlers[crawler_type]
                if self.is_match(url, job_site):
                    logging.debug('Match found: ' + url + ' with ' + job_site)
                    class_name = crawler_type
                    module_name = self.package_name + '.' + class_name
                    crawler_module = import_module(module_name)
                    crawler_class = getattr(crawler_module, class_name)
                    crawler_instance = crawler_class(job)
        except Exception as e:
            logging.error('Unable to retrieve a crawler instance: ' + str(e))
            raise
        return crawler_instance

    @staticmethod
    def is_match(url, job_site):
        if not url:
            raise ValueError('No url exists in job description')
        return url.find(job_site) != -1


'''''
        indeed = job.url.find('ca.indeed.com') != -1
        talgroup = job.url.find('talgroup.net') != -1
        workday = job.url.find('myworkdayjobs.com') != -1
        aerotek = job.url.find('www.aplitrak.com') != -1
        smoothhiring = job.url.find('app.smoothhiring.com') != -1
        rbc = job.url.find('jobs.rbc.com') != -1
        brassring = job.url.find('krb-sjobs.brassring.com') != -1
        eagle = job.url.find('jobs.eagleonline.com') != -1
        taleo = job.url.find('taleo.net') != -1
        david_aplin = job.url.find('www.aplin.com') != -1
        adp = job.url.find('workforcenow.adp.com') != -1
        jobdiva = job.url.find('jobdiva.com') != -1
        recruitinginmotion = job.url.find('recruitinginmotion.com') != -1
        webconnect = job.url.find('webconnect.sendouts.net') != -1
        akamai = job.company.find('Akamai') != -1
        ian_martin = job.url.find('careers.ianmartin.com') != -1
        teksystems = job.url.find('www.teksystems.com') != -1
        hire_google = job.url.find('hire.withgoogle.com') != -1
        google = job.url.find('careers.google.com') != -1
'''''
