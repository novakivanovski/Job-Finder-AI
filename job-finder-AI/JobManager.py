from Utilities import QueueUnpacker, ParsingUtilities
import logging
from DataStructures.Job import Job


class JobManager:
    def __init__(self, crawler, lister):
        self.jobs = []
        self.failed_jobs = []
        self.num_jobs = 0
        self.job_id = 0
        self.crawler = crawler
        self.lister = lister

    def get_jobs(self):
        listings = self.get_job_listings()
        postings = self.get_job_postings(listings)
        logging.debug("Job postings with descriptions: " + str(len(postings)))
        jobs = self.get_jobs_from_postings(postings)
        jobs_with_keywords = self.update_jobs_with_keywords(jobs)
        self.set_jobs(jobs_with_keywords)
        return jobs_with_keywords

    def get_job_listings(self):
        page_listings_queue = self.crawler.crawl_job_listings()
        page_listings = QueueUnpacker.unpack(page_listings_queue)
        self.lister.add_pages(page_listings)
        listings = self.lister.get_listings()
        return listings

    def update_jobs_with_keywords(self, jobs):
        self.failed_jobs = ParsingUtilities.remove_and_get_empty(jobs)
        logging.debug('Failed jobs: ' + str(self.failed_jobs))
        jobs_with_keywords = ParsingUtilities.update_keywords(jobs)
        return jobs_with_keywords

    def get_job_postings(self, listings):
        posting_queue = self.crawler.crawl_job_postings(listings)
        postings = QueueUnpacker.unpack(posting_queue)
        return postings

    def get_jobs_from_postings(self, postings):
        jobs = []
        for posting in postings:
            job = Job(posting)
            jobs.append(job)
        logging.debug('Created ' + str(len(jobs)) + ' jobs from postings.')
        return self.update_job_descriptions(jobs)

    def update_job_descriptions(self, jobs):
        jobs_queue = self.crawler.crawl_job_descriptions(jobs)
        jobs = QueueUnpacker.unpack(jobs_queue)
        return jobs

    def set_jobs(self, jobs):
        self.jobs = jobs
        self.num_jobs = len(jobs)

    def get_num_jobs(self):
        return self.num_jobs

    def clear_jobs(self):
        self.jobs = []

