from math import ceil
import re
import logging
from Utilities import NetworkUtilities
from Crawlers.BaseCrawler import BaseCrawler
from DataStructures.Posting import Posting
from Utilities.ApplicationExceptions import CrawlerError


class GenericCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()

    def get_listings(self):  # Override
        pass

    def configure(self):  # Override
        pass

    def get_number_of_jobs(self, html_text):
        try:
            search_result = re.search(self.jobs_regex, html_text)[0]
            number_of_jobs = self.extract_number_of_jobs(search_result)
            logging.debug('Number of jobs: ' + str(number_of_jobs))
        except Exception:
            raise CrawlerError('Unable to get number of jobs.')
        return number_of_jobs

    def extract_number_of_jobs(self, search_result):  # Override
        return 0

    def get_num_pages(self, num_jobs):
        num_pages = ceil(num_jobs / self.jobs_per_page)
        return int(num_pages)

    def crawl_job_listing_page(self, page_number):
        url = self.get_page_url(page_number)
        listing_page = NetworkUtilities.get_page(url)
        return listing_page

    def get_page_url(self, page_number):  # Override
        return ''

    def crawl_job_posting_page(self, listing):
        try:
            posting_url = listing.get_url()
            page = NetworkUtilities.get_page(posting_url)
            posting = Posting(listing, page)
        except Exception:
            raise CrawlerError('Error crawling job posting.')
        return posting

    def crawl_job_listings(self):
        html_text = NetworkUtilities.get_html(self.entry_url)
        self.num_jobs = self.get_number_of_jobs(html_text)
        self.num_pages = self.get_num_pages(self.num_jobs)
        self.MultiThreader.run_queue_monitor(self.num_pages)

        for page_num in range(self.num_pages):
            self.MultiThreader.add_thread(self.crawl_job_listing_page, page_num)
        page_listings_queue = self.MultiThreader.schedule_threads()
        return page_listings_queue

    def crawl_job_postings(self, listings):
        num_jobs = len(listings)
        logging.debug('Crawling ' + str(num_jobs) + ' job postings...')
        for listing in listings:
            logging.debug('Adding job posting crawler thread: ' + str(listing.get_id()))
            self.MultiThreader.add_thread(self.crawl_job_posting_page, listing)

        self.MultiThreader.run_queue_monitor(num_jobs)
        job_posting_queue = self.MultiThreader.schedule_threads()
        return job_posting_queue

    def crawl_job_descriptions(self, jobs):
        num_jobs = len(jobs)
        logging.debug('Crawling ' + str(num_jobs) + ' job descriptions...')
        self.MultiThreader.run_queue_monitor(num_jobs)
        for job in jobs:
            logging.debug('Adding job description crawler thread: ' + str(job.get_id()))
            self.MultiThreader.add_thread(self.crawl_job_description, job)
        updated_jobs = self.MultiThreader.schedule_threads()
        return updated_jobs

    def crawl_job_description(self, job):
        try:
            description_crawler = self.description_crawler_factory.get(job)
            raw_text = description_crawler.get_description()
            job.set_plaintext(raw_text)
        except Exception as e:
            logging.error('Error crawling job description: ' + str(e))
        return job





