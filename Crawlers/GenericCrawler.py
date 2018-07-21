from math import ceil
import re
import logging
from Utilities import NetworkUtilities
from Crawlers.BaseCrawler import BaseCrawler


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
        except Exception as e:
            logging.error('Error - unable to find number of jobs: ' + str(e))
            raise
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

    def crawl_job_posting_page(self, job):
        try:
            entry_url = job.get_entry_url()
            response = NetworkUtilities.get(entry_url)
            response_url = response.url
            job.set_plaintext(response.text)
            job.set_url(response_url)
        except Exception as e:
            logging.error('No response crawling job posting ' + str(e))
        return job

    def crawl_job_listings(self):
        html_text = NetworkUtilities.get_html(self.entry_url)
        self.num_jobs = self.get_number_of_jobs(html_text)
        self.num_pages = self.get_num_pages(self.num_jobs)
        self.MultiThreader.run_queue_monitor(self.num_pages)

        for page_num in range(self.num_pages):
            self.MultiThreader.add_thread(self.crawl_job_listing_page, page_num)
        page_listings_queue = self.MultiThreader.schedule_threads()
        return page_listings_queue

    def crawl_job_postings(self, jobs):
        num_jobs = len(jobs)
        logging.debug('Crawling ' + str(num_jobs) + ' job postings...')
        for job in jobs:
            logging.debug('Adding job posting crawler thread: ' + str(job.get_id()))
            self.MultiThreader.add_thread(self.crawl_job_posting_page, job)

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
            if job.has_description():
                description_crawler = self.description_crawler_factory.get(job)
                raw_text = description_crawler.get_plaintext()
                job.set_raw(raw_text)
            else:
                logging.debug('Job has no description: ' + str(job.get_id()))
        except Exception as e:
            logging.error('Error crawling job description: ' + str(e))
        return job





