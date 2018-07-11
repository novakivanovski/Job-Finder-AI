from Job import Job
from JobParser import JobParser
import MultiThreader
from QueueUnpacker import QueueUnpacker


class JobManager:
    def __init__(self, crawler):
        self.jobs = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        self.num_jobs = 0
        self.job_id = 0
        self.crawler = crawler
        self.helpers = None
        self.parser = JobParser(None)
        self.MultiThreader = MultiThreader.MultiThreader()

    def obtain_jobs(self): 
        metadata = self.get_jobs_metadata()
        jobs_with_metadata = self.make_jobs_from_metadata(metadata)
        jobs_with_descriptions = self.update_jobs_with_descriptions(jobs_with_metadata)
        jobs = self.process_jobs(jobs_with_descriptions)
        self.set_jobs(jobs)
        return jobs

    def get_jobs_metadata(self):
        job_listings_queue = self.crawler.crawl_job_listings()
        job_listings_soups = QueueUnpacker.unpack_to_soup(job_listings_queue)
        jobs_metadata = JobParser.get_metadata(job_listings_soups)
        return jobs_metadata
    
    def process_jobs(self, jobs):
        non_empty_jobs = self.parser.remove_empty(jobs)
        for job in non_empty_jobs:
            keywords = self.parser.get_keywords(job)
            job.set_keywords(keywords)
        return non_empty_jobs  # keep the empty jobs somewhere for debugging?
            
    def update_jobs_with_descriptions(self, jobs):
        updated_job_queue = self.crawler.crawl_job_postings(jobs)
        jobs_with_descriptions = QueueUnpacker.unpack(updated_job_queue)
        return jobs_with_descriptions

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

    def obtain_job_descriptions(self):
        for job in self.jobs:
            self.MultiThreader.add_thread(self.helpers.get_raw, job)
        self.MultiThreader.add_queue_monitor_thread(self.num_jobs)
        self.MultiThreader.schedule_threads()

        for job in self.jobs:
            keywords = self.parser.extract_keywords(job)
            job.set_keywords(keywords)


