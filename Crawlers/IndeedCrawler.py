from Crawlers.GenericCrawler import GenericCrawler


class IndeedCrawler(GenericCrawler):
    def __init__(self):
        super().__init__()

    def configure(self):
        self.jobs_per_page = 50
        self.jobs_regex = 'Jobs 1 to 50 of .+\d'
        self.page_addend = '&start='
        self.base_url = 'https://www.indeed.ca'
        self.entry_url = 'https://www.indeed.ca/jobs?q=engineer&l=Toronto%2C+ON&limit=50&fromage=3&radius=50'

    def extract_number_of_jobs(self, search_result):
        search_result = search_result.replace(",", "")
        number_of_jobs = int(search_result[16:])
        return number_of_jobs

    def get_page_url(self, page_number):
        page_url = self.entry_url + self.page_addend + str(page_number * self.jobs_per_page)
        return page_url



