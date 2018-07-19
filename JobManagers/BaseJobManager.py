from Job import Job
from Utilities import MultiThreader, QueueUnpacker, ParsingUtilities
import logging
from Listings import ListingsFactory
from abc import ABC


class BaseJobManager(ABC):
    def __init__(self, crawler, listing_type):
        self.jobs = []
        self.failed_jobs = []
        self.num_jobs = 0
        self.job_id = 0
        self.crawler = crawler
        self.MultiThreader = MultiThreader.MultiThreader()
        self.listing_type = listing_type  # (e.g. EngineerJobsListings)

    def obtain_jobs(self): 
        metadata = self.get_jobs_metadata()
        jobs_with_metadata = self.make_jobs_from_metadata(metadata)
        jobs_with_descriptions = self.update_jobs_with_descriptions(jobs_with_metadata)
        logging.debug("Jobs with descriptions: " + str(len(jobs_with_descriptions)))
        jobs = self.process_jobs(jobs_with_descriptions)
        self.set_jobs(jobs)
        return jobs

    def get_jobs_metadata(self):
        job_listings_text_queue = self.crawler.crawl_job_listings()
        job_listings_text = QueueUnpacker.unpack(job_listings_text_queue)
        job_listings = ListingsFactory.get(job_listings_text, self.listing_type)
        jobs_metadata = job_listings.get_metadata()
        return jobs_metadata
    
    def process_jobs(self, jobs):
        empty_jobs = ParsingUtilities.remove_and_get_empty(jobs)
        self.failed_jobs = empty_jobs
        for job in jobs:
            keywords = ParsingUtilities.get_keywords(job)
            job.set_keywords(keywords)
        return jobs
            
    def update_jobs_with_descriptions(self, jobs):
        updated_job_queue = self.crawler.crawl_job_postings(jobs)
        jobs_with_descriptions = QueueUnpacker.unpack(updated_job_queue)
        updated_job_queue = self.crawler.crawl_job_descriptions(jobs_with_descriptions)
        updated_jobs = QueueUnpacker.unpack(updated_job_queue)
        return updated_jobs

    def make_jobs_from_metadata(self, metadata):
        jobs = []
        for m in metadata:
            job_id = self.generate_job_id()
            m.set_id(job_id)
            job = Job(m)
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

