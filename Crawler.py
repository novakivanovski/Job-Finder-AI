import requests
from math import ceil
from bs4 import BeautifulSoup
import re
from Job import Job
import logging
from multiprocessing import Process, Manager, Pool as ThreadPool
from threading import Thread
from time import time, sleep
from FilterAlgorithm import FilterAlgorithm
from Job import Job, JobMetadata
from JobManager import JobManager
from MultiThreader import MultiThreader
import IOUtils


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
        url = self.entry_url + str(page_number + 1)
        soup = IOUtils.get_soup_from_url(url)
        self.extract_jobs_from_page_soup(soup)

    def extract_jobs_from_page_soup(self, page_soup):
        for job_entry in page_soup.find_all(class_="jobrow"):
            job_data = []
            items = job_entry.find_all('td')
            for item in items:
                job_data.append(item.text)
            metadata = JobMetadata(url=job_data[0], title=job_data[1], location=job_data[2],
                                   company=job_data[3], date=job_data[4])
            self.JobManager.add_job(metadata)

    def percent_complete(self, max_size, q, bar):
        q_size = 0
        while q_size < max_size:
            q_size = q.qsize()
            self.percents[bar] = (q_size / max_size) * 100
            sleep(1)

    def multi_thread(self):
        q = Manager().Queue(maxsize=0)
        self.MultiThreader.add_thread(target=self.percent_complete, args =(self.num_jobs, q, 0))
        self.MultiThreader.run_threads()

        for page_num in range(self.num_pages):
            t = Thread(target=self.get_job_details, args=(page_num, q))
            threads.append(t)
            t.start()
        
        for thrd in threads:
            thrd.join()

        threads = []
        
        while not q.empty():
            self.details.append(q.get())

        for job in self.details:
            t = Thread(target=self.create_jobs, args =(q, job))
            threads.append(t)
            
        num_threads = len(threads)
        num_passes = int(ceil(num_threads/max_threads))
        loading = Thread(target=self.percent_complete, args=(num_threads, 1, q))
        loading.start()

        for k in range(num_passes):
            start = k * max_threads
            end = (k + 1) * max_threads
            for i in range(start, end):
                if i < num_threads:
                    threads[i].start()
            for i in range(start, end):
                if i < num_threads:
                    threads[i].join()

        loading.join()

        while not q.empty():
            self.jobs.append(q.get())
        
        loading = Thread(target=self.percent_complete, args=(num_threads, 2, q))
        loading.start()
        self.f.extract(self.jobs, q)
        self.num_jobs = len (self.jobs)
        loading.join()

     
    def crawl(self):
        html_soup = IOUtils.get_soup_from_url(self.entry_url)
        self.get_number_of_jobs_and_pages_from_soup(html_soup)
        self.entry_html_soup = html_soup
        self.multi_thread()