from Job import Job, JobDescription
from JobParser import JobParser
import MultiThreader
from QueueUnpacker import QueueUnpacker
import logging

class JobManager:
    def __init__(self, crawler):
        self.jobs = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        self.num_jobs = 0
        self.job_id = 0
        self.crawler = crawler
        self.helpers = None
        self.parser = JobParser('keywords_file_path.txt')
        self.MultiThreader = MultiThreader.MultiThreader()

    def obtain_jobs(self):   # make a new class just for creating the metadata, description?
        metadata = self.get_jobs_metadata()
        jobs = self.make_jobs_from_metadata(metadata)
        self.set_jobs(jobs)
        descriptions_added = self.set_job_descriptions(self.jobs)
        descriptions_updated = self.update_job_descriptions(self.jobs)
        logging.debug('Number of jobs: ' + str(self.num_jobs))
        logging.debug('Descriptions added: ' + str(descriptions_added))
        logging.debug('Descriptions updated: ' + str(descriptions_updated))
        non_empty_jobs = self.parser.remove_empty(self.jobs)
        self.set_jobs(non_empty_jobs)
        logging.debug('Number of non empty jobs: ' + str(self.num_jobs))

    def get_jobs_metadata(self):
        job_listings_queue = self.crawler.crawl_job_listings()
        job_listings_soups = QueueUnpacker.unpack_to_soup(job_listings_queue)
        jobs_metadata = JobParser.get_metadata(job_listings_soups)
        return jobs_metadata

    def set_job_descriptions(self, jobs):
        job_postings_queue = self.crawler.crawl_job_postings(jobs)
        descriptions_added = len(QueueUnpacker.unpack(job_postings_queue))
        return descriptions_added

    def update_job_descriptions(self, jobs):
        description_queue = self.crawler.crawl_job_descriptions(jobs)
        descriptions_updated = len(QueueUnpacker.unpack(description_queue))
        for job in jobs:
            keywords = self.parser.extract_keywords(job)
            job.set_keywords(keywords)
        return descriptions_updated

    def make_jobs_from_metadata(self, metadata):
        jobs = []
        for m in metadata:
            description = JobDescription(None)
            job_id = self.generate_job_id()
            m.set_id(job_id)
            job = Job(m, description)
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

    def obtain_job_descriptions(self):
        for job in self.jobs:
            self.MultiThreader.add_thread(self.helpers.get_raw, job)
        self.MultiThreader.add_queue_monitor_thread(self.num_jobs)
        self.MultiThreader.schedule_threads()

        for job in self.jobs:
            keywords = self.parser.extract_keywords(job)
            job.set_keywords(keywords)


