from Utilities import QueueUnpacker, ParsingUtilities
import logging
from abc import ABC
from DataStructures.Job import Job


class BaseJobManager(ABC):
    def __init__(self, crawler, lister):
        self.jobs = []
        self.failed_jobs = []
        self.num_jobs = 0
        self.job_id = 0
        self.crawler = crawler
        self.lister = lister  # (e.g. EngineerJobsLister)

    def obtain_jobs(self): 
        listings = self.get_job_listings()
        postings = self.get_job_postings(listings)
        logging.debug("Job postings with descriptions: " + str(len(postings)))
        jobs = self.get_jobs_from_postings(postings)
        self.set_jobs(jobs)
        return jobs

    def get_job_listings(self):
        page_listings_queue = self.crawler.crawl_job_listings()
        page_listings = QueueUnpacker.unpack(page_listings_queue)
        self.lister.add_pages(page_listings)
        listings = self.lister.get_listings()
        return listings
    
    def process_jobs(self, jobs):
        empty_jobs = ParsingUtilities.remove_and_get_empty(jobs)
        self.failed_jobs = empty_jobs
        for job in jobs:
            keywords = ParsingUtilities.get_keywords(job)
            job.set_keywords(keywords)
        return jobs
            
    def get_job_postings(self, listings):
        posting_queue = self.crawler.crawl_job_postings(listings)
        postings = QueueUnpacker.unpack(posting_queue)
        postings_with_descriptions_queue = self.crawler.crawl_job_descriptions(postings)
        postings_with_descriptions = QueueUnpacker.unpack(postings_with_descriptions_queue)
        return postings_with_descriptions

    @staticmethod
    def get_jobs_from_postings(postings):
        jobs = []
        for posting in postings:
            job = Job(posting)
            jobs.append(job)
        return jobs

    def set_jobs(self, jobs):
        self.jobs = jobs
        self.num_jobs = len(jobs)

    def get_num_jobs(self):
        return self.num_jobs

    def generate_job_id(self):
        self.job_id += 1
        return self.job_id

    def clear_jobs(self):
        self.jobs = []

