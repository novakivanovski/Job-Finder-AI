from time import time
from JobManager import JobManager
from Storage.Storage import Storage
from Crawlers import EngineerJobsCrawler
from DataStructures.Listers import EngineerJobsLister
import os


def run():
    start = time()
    project_path = os.getcwd()
    storage = Storage(project_path)
    crawler = EngineerJobsCrawler.EngineerJobsCrawler()
    lister = EngineerJobsLister.EngineerJobsLister()
    manager = JobManager(crawler, lister)
    jobs = manager.get_jobs()
    storage.store_jobs(jobs)
    retrieved_jobs = storage.retrieve_jobs()
    for job in retrieved_jobs:
        print(job.get_title())
    elapsed = round((time() - start), 2)
    print('Elapsed time: ' + str(elapsed) + ' seconds')