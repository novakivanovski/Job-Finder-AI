from time import time
from JobManagers.Managers import EngineerJobsManager


def run():
    start = time()
    manager = EngineerJobsManager()
    storage = manager.storage
    jobs = manager.get_jobs()
    storage.store_jobs(jobs)
    retrieved_jobs = storage.get_jobs_from_cache()
    for job in retrieved_jobs:
        print(job.get_title())
    elapsed = round((time() - start), 2)
    print('Elapsed time: ' + str(elapsed) + ' seconds')