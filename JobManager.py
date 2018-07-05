from Job import Job, JobDescription
import logging
from bs4 import BeautifulSoup
import Helpers
import JobParser
import MultiThreader


class JobPackage:
    def __init__(self, html, metadata, job_id):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.metadata = metadata
        self.metadata.job_id = job_id


class JobManager:
    def __init__(self, crawler):
        self.jobs = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        self.num_jobs = 0
        self.job_id = 0
        self.crawler = crawler
        self.helpers = Helpers.Helpers()
        self.parser = JobParser.JobParser('keywords_file_path.txt')
        self.MultiThreader = MultiThreader.MultiThreader()

    def obtain_jobs(self):
        metadata_queue = self.crawler.crawl_pages()
        jobs_metadata = self.unpack_metadata_queue(metadata_queue)
        jobs_queue = self.crawler.crawl_jobs(jobs_metadata)
        jobs_text = self.unpack_queue(jobs_queue)
        job_packages = self.create_job_packages(jobs_text, jobs_metadata)
        self.jobs = self.make_jobs_from_packages(job_packages)
        return self.jobs

    def create_job_packages(self, texts, jobs_metadata):
        packages = []
        for text, metadata in zip(texts, jobs_metadata):
            job_id = self.generate_job_id()
            package = JobPackage(text, metadata, job_id)
            packages.append(package)
        return packages

    def unpack_metadata_queue(self, metadata_queue):
        metadata_lists = self.unpack_queue(metadata_queue)
        metadata = self.flatten_list(metadata_lists)
        return metadata

    @staticmethod
    def unpack_queue(queue):
        items = []
        while not queue.empty():
            try:
                queue_item = queue.get()
                items.append(queue_item)
            except Exception as e:
                logging.error(e)
        return items

    @staticmethod
    def flatten_list(lists):
        flattened_list = []
        for this_list in lists:
            for this_item in this_list:
                flattened_list.append(this_item)
        return flattened_list

    @staticmethod
    def make_jobs_from_packages(packages):
        jobs = []
        for package in packages:
            metadata = package.metadata
            description = JobDescription(package.soup)
            job = Job(metadata, description)
            jobs.append(job)
        return jobs

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
            self.parser.filter_job_and_get_keywords(job)
        self.jobs = self.parser.remove_empty(self.jobs)

