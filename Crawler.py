from math import ceil
import re
import logging
from MultiThreader import MultiThreader
import NetworkUtilities
from JobParser import JobParser


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
        self.configure(url)

    def configure(self, url):  # override this method for LinkedInCrawler, IndeedCrawler
        self.jobs_per_page = 20
        self.jobs_regex = '\d+ Jobs'
        self.page_addend = '&page='
        self.entry_url = url
        self.base_url = 'https://www.engineerjobs.com'

    def get_number_of_jobs_and_pages_from_soup(self, html_soup):
        self.num_jobs = self.get_number_of_jobs(html_soup)
        self.num_pages = self.get_num_pages(self.num_jobs)

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
        return ceil(num_jobs / self.jobs_per_page)

    def crawl_job_listing_page(self, page_number):
        url = self.entry_url + '&page=' + str(page_number + 1)
        listings_soup = NetworkUtilities.get_soup_from_url(url)
        metadata = JobParser.get_metadata_from_page_soup(listings_soup, self.base_url)
        return metadata

    @staticmethod
    def crawl_job_posting_page(metadata):
        posting = NetworkUtilities.get_html_from_url(metadata.origin_url)
        return posting

    def crawl_pages(self):
        self.crawl_first_page()
        self.MultiThreader.add_queue_monitor_thread(self.num_pages)

        for page_num in range(self.num_pages):
            self.MultiThreader.add_thread(self.crawl_job_listing_page, page_num)
        metadata_queue = self.MultiThreader.schedule_threads()
        return metadata_queue

    def crawl_first_page(self):
        html_soup = NetworkUtilities.get_soup_from_url(self.entry_url)
        self.get_number_of_jobs_and_pages_from_soup(html_soup)

    def crawl_jobs(self, jobs_metadata):
        for metadata in jobs_metadata:
            self.MultiThreader.add_thread(self.crawl_job_posting_page, metadata)

        self.MultiThreader.add_queue_monitor_thread(self.num_jobs)
        jobs_text = self.MultiThreader.schedule_threads()
        return jobs_text


