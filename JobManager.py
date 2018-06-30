from Job import Job, JobDescription
import NetworkUtilities


class JobPackage:
    def __init__(self, soup, metadata, job_id):
        self.soup = soup
        self.metadata = metadata
        self.metadata.job_id = job_id


class JobManager:
    def __init__(self, crawler):
        self.jobs = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        self.num_jobs = 0
        self.job_id = 0
        self.crawler = crawler

    def obtain_jobs(self):
        listings = self.crawler.crawl_pages()
        jobs_metadata = self.get_metadata_from_queue(listings)
        jobs_soup = self.crawler.crawl_jobs(jobs_metadata)
        job_packages = self.create_job_packages(jobs_soup, jobs_metadata)
        self.jobs = self.make_jobs_from_packages(job_packages)
        return self.jobs

    def create_job_packages(self, soups, jobs_metadata):
        packages = []
        for soup, metadata in zip(soups, jobs_metadata):
            job_id = self.generate_job_id()
            package = JobPackage(soup, metadata, job_id)
            packages.append(package)
        return packages

    @staticmethod
    def get_metadata_from_queue(queue):
        jobs_metadata = []
        while not queue.empty():
            metadata = queue.get()
            jobs_metadata.append(metadata)
        return jobs_metadata

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

    @staticmethod
    def update_job_description(job):
        description_text = NetworkUtilities.get_html_from_url(job.entry_url)
        description = JobDescription(description_text)
        job.description = description

    def clear_jobs(self):
        self.jobs = []

    @staticmethod
    def update_title(job, title):
        job.title = title

    @staticmethod
    def update_location(job, location):
        job.location = location

    @staticmethod
    def update_metadata(metadata, job):
        job.metadata = metadata
