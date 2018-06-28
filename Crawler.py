from math import ceil
import re
import logging
from multiprocessing import Manager
from FilterAlgorithm import FilterAlgorithm
from Job import JobMetadata
from JobManager import JobManager
from MultiThreader import MultiThreader
import IOUtils
from QueueMonitor import QueueMonitor


class Crawler:
    def __init__(self, url, file_path=''):
        self.jobs = []
        self.details = []
        self.num_jobs = 0
        self.f = None
        self.jobs_per_page = 1
        self.percents = [0, 0, 0]
        self.num_pages = 0
        self.jobs_regex = ''
        self.threads = []
        self.entry_url = None
        self.entry_html_soup = None
        self.details = []
        self.JobManager = JobManager()
        self.MultiThreader = MultiThreader()
        self.configure(url, file_path)

    def configure(self, url, file_path):  # override this method for LinkedInCrawler, IndeedCrawler
        self.jobs_per_page = 20
        self.jobs_regex = '\d+ Jobs'
        self.entry_url = url
        self.f = FilterAlgorithm(file_path)

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
        soup = IOUtils.get_soup_from_url(url)
        metadata = self.get_metadata_from_page_soup(soup)
        return metadata

    @staticmethod
    def get_metadata_from_page_soup(page_soup):
        metadata = None
        for job_entry in page_soup.find_all(class_="jobrow"):
            job_data = []
            items = job_entry.find_all('td')
            for item in items:
                job_data.append(item.text)
                logging.debug(item.text)

            metadata = JobMetadata(url=None, title=job_data[0], location=job_data[1],
                                   company=job_data[2], date=job_data[3])
        return metadata

    def load_pages(self):  # need to be revamped further - indexer class to hold num pages?
        self.MultiThreader.add_queue_monitor_thread(self.num_pages)

        for page_num in range(self.num_pages):
            self.MultiThreader.add_thread(self.crawl_job_listing_page, page_num)
        self.MultiThreader.schedule_threads()
        self.JobManager.add_jobs_from_queue(self.MultiThreader.queue)

    def load_jobs(self):
        queue = Manager().Queue()
        for job in self.JobManager.jobs:
            self.MultiThreader.add_thread(self.JobManager.update_job_description, queue, job)

        jobs_load = QueueMonitor(queue, self.num_jobs) 
        self.MultiThreader.add_thread(jobs_load.start)  # don't make daemon so it can be joined
        self.MultiThreader.schedule_threads()
        self.f.extract(self.jobs, queue)
        self.num_jobs = len(self.jobs)

    def parse_jobs(self):
        queue = Manager().Queue()
        self.f.extract(self.jobs, queue)
        self.num_jobs = len(self.jobs)

    def crawl(self):
        html_soup = IOUtils.get_soup_from_url(self.entry_url)
        self.get_number_of_jobs_and_pages_from_soup(html_soup)
        self.entry_html_soup = html_soup
        self.load_pages()
        self.parse_jobs()
