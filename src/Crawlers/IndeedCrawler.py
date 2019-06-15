from Crawlers.GenericCrawler import GenericCrawler


class IndeedCrawler(GenericCrawler):
    def __init__(self, days=1):
        super().__init__(days)

    def configure(self):
        self.jobs_per_page = 50
        self.jobs_regex = '1( to 50)? of ((\d|,)+)'
        self.page_addend = '&start='
        self.base_url = 'https://www.indeed.ca'
        self.entry_url = self.base_url + '/jobs?as_and=software+engineer&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&' \
                                         'jt=all&st=&as_src=&salary=&radius=100&l=Milton,+ON&fromage=' \
                                         + str(self.days) + '&limit=50&sort=&psf=advsrch'

    def extract_number_of_jobs(self, search_result):
        second_group = search_result.group(2)
        number_of_jobs = second_group.replace(",", "")
        return int(number_of_jobs)

    def get_page_url(self, page_number):
        page_url = self.entry_url + self.page_addend + str(page_number * self.jobs_per_page)
        return page_url



