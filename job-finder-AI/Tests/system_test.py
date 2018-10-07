from time import time
from JobManager import JobManager
from Storage.LocalStorage import LocalStorage
from Crawlers import EngineerJobsCrawler
from DataStructures.Listers import EngineerJobsLister


def run():
    start = time()
    storage = LocalStorage()
    crawler = EngineerJobsCrawler.EngineerJobsCrawler()
    lister = EngineerJobsLister.EngineerJobsLister()
    manager = JobManager(crawler, lister)
    jobs = manager.get_jobs()
    storage.store_jobs(jobs)
    retrieved_jobs = storage.get_jobs_from_cache()
    for job in retrieved_jobs:
        print(job.get_title())
    elapsed = round((time() - start), 2)
    print('Elapsed time: ' + str(elapsed) + ' seconds')