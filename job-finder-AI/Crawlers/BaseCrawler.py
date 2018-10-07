from abc import ABC, abstractmethod
from Utilities.MultiThreader import MultiThreader
from PostingCrawlers.PostingCrawlerFactory import PostingCrawlerFactory


class BaseCrawler(ABC):
    def __init__(self, days=1):
        self.days = days
        self.jobs = []
        self.details = []
        self.num_jobs = None
        self.jobs_per_page = None
        self.num_pages = None
        self.jobs_regex = ''
        self.page_addend = ''
        self.threads = []
        self.entry_url = ''
        self.base_url = ''
        self.details = []
        self.MultiThreader = MultiThreader()
        self.description_crawler_factory = PostingCrawlerFactory()
        self.configure()

    @abstractmethod
    def configure(self):  # Override
        pass

    @abstractmethod
    def get_number_of_jobs(self, html_text):
        pass

    @abstractmethod
    def extract_number_of_jobs(self, search_result):  # Override
        pass

    @abstractmethod
    def get_num_pages(self, num_jobs):
        pass

    @abstractmethod
    def crawl_job_listing_page(self, page_number):
        pass

    @abstractmethod
    def crawl_job_posting_page(self, job):
        pass

    @abstractmethod
    def crawl_job_listings(self):
        pass

    @abstractmethod
    def crawl_job_postings(self, jobs):
        pass

    @abstractmethod
    def crawl_job_descriptions(self, jobs):
        pass

    @abstractmethod
    def crawl_job_description(self, job):
        pass





