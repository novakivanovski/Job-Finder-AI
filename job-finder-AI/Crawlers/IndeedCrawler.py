from Crawlers.GenericCrawler import GenericCrawler


class IndeedCrawler(GenericCrawler):
    def __init__(self, days=1):
        super().__init__(days)

    def configure(self):
        self.jobs_per_page = 50
        self.jobs_regex = 'Jobs .+ of ((\d|,)+)'
        self.page_addend = '&start='
        self.base_url = 'https://www.indeed.ca'
        self.entry_url = self.base_url + '/jobs?q=engineer&l=Toronto%2C+ON&limit=50&fromage=' + \
                         str(self.days) + '&filter=0&radius=50'

    def extract_number_of_jobs(self, search_result):
        number_of_jobs = search_result.replace(",", "")
        return int(number_of_jobs)

    def get_page_url(self, page_number):
        page_url = self.entry_url + self.page_addend + str(page_number * self.jobs_per_page)
        return page_url



