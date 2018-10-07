from Crawlers.GenericCrawler import GenericCrawler


class EngineerJobsCrawler(GenericCrawler):
    def __init__(self, days=1):
        super().__init__(days)

    def configure(self):
        self.jobs_per_page = 20
        self.jobs_regex = '((\d|,)+) Jobs'
        self.page_addend = '&page='
        self.base_url = 'https://www.engineerjobs.com'
        self.entry_url = self.base_url + '/jobs/software-engineering/canada/ontario/?f=' + str(self.days)

    def extract_number_of_jobs(self, search_result):
        number_of_jobs = search_result.replace(',', '')
        return int(number_of_jobs)

    def get_page_url(self, page_number):
        page_url = self.entry_url + self.page_addend + str(page_number + 1)
        return page_url



