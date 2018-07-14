from math import ceil
import re
import logging
from MultiThreader import MultiThreader
import NetworkUtilities
from DescriptionCrawlerFactory import DescriptionCrawlerFactory


class Crawler:
    def __init__(self, url):
        self.jobs = []
        self.details = []
        self.num_jobs = 0
        self.jobs_per_page = 1
        self.num_pages = 0
        self.jobs_regex = ''
        self.page_addend = ''
        self.threads = []
        self.entry_url = None
        self.base_url = None
        self.details = []
        self.MultiThreader = MultiThreader()
        self.description_crawler_factory = DescriptionCrawlerFactory()
        self.configure(url)

    def configure(self, url):  # override this method for LinkedInCrawler, IndeedCrawler
        self.jobs_per_page = 20
        self.jobs_regex = '\d+ Jobs'
        self.page_addend = '&page='
        self.entry_url = url
        self.base_url = 'https://www.engineerjobs.com'

    def get_number_of_jobs(self, html_soup):
        try:
            search_result = re.search(self.jobs_regex, html_soup.text)[0]
            number_of_jobs = int(search_result[:-5])
            logging.debug('Number of jobs: ' + str(number_of_jobs))
        except Exception as e:
            number_of_jobs = 0
            logging.error('Error - unable to find number of jobs: ' + str(e))
        return number_of_jobs

    def get_num_pages(self, num_jobs):
        num_pages = ceil(num_jobs / self.jobs_per_page)
        return int(num_pages)

    def crawl_job_listing_page(self, page_number):
        url = self.entry_url + self.page_addend + str(page_number + 1)
        job_listings = NetworkUtilities.get_html(url)
        return job_listings

    @staticmethod
    def crawl_job_posting_page(job):
        try:
            entry_url = job.get_entry_url()
            response = NetworkUtilities.get(entry_url)
            response_url = response.url
            job.set_description(response.text)
            job.set_url(response_url)
        except Exception as e:
            logging.error('No response crawling job posting ' + str(e))
        return job

    def crawl_job_listings(self):
        html_soup = NetworkUtilities.get_soup(self.entry_url)
        self.num_jobs = self.get_number_of_jobs(html_soup)
        self.num_pages = self.get_num_pages(self.num_jobs)
        self.MultiThreader.add_queue_monitor_thread(self.num_pages)

        for page_num in range(self.num_pages):
            self.MultiThreader.add_thread(self.crawl_job_listing_page, page_num)
        job_listings_queue = self.MultiThreader.schedule_threads()
        return job_listings_queue

    def crawl_job_postings(self, jobs):
        num_jobs = len(jobs)
        logging.debug('Crawling ' + str(num_jobs) + ' job postings...')
        for job in jobs:
            logging.debug('Adding job posting crawler thread: ' + str(job.get_id()))
            self.MultiThreader.add_thread(self.crawl_job_posting_page, job)

        self.MultiThreader.add_queue_monitor_thread(num_jobs)
        job_posting_queue = self.MultiThreader.schedule_threads()
        return job_posting_queue

    def crawl_job_descriptions(self, jobs):
        num_jobs = len(jobs)
        logging.debug('Crawling ' + str(num_jobs) + ' job descriptions...')
        self.MultiThreader.add_queue_monitor_thread(num_jobs)
        for job in jobs:
            logging.debug('Adding job description crawler thread: ' + str(job.get_id()))
            self.MultiThreader.add_thread(self.crawl_job_description, job)
        updated_jobs = self.MultiThreader.schedule_threads()
        return updated_jobs

    def crawl_job_description(self, job):
        try:
            if job.has_description():
                description_crawler = self.description_crawler_factory.get(job)
                raw_text = description_crawler.get_description()
                job.set_raw(raw_text)
            else:
                logging.debug('Job has no description: ' + str(job.get_id()))
        except Exception as e:
            logging.error('Error crawling job description: ' + str(e))
        return job





