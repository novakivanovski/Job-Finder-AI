from Crawlers.GenericCrawler import GenericCrawler


class LinkedInCrawler(GenericCrawler):  # Not implemented yet
    def __init__(self):
        super().__init__()

    def configure(self):
        self.jobs_per_page = ''
        self.jobs_regex = ''
        self.page_addend = ''
        self.base_url = 'https://www.linkedin.com/'
        self.entry_url = ''

    def extract_number_of_jobs(self, search_result):
        pass

    def get_page_url(self, page_number):
        pass


