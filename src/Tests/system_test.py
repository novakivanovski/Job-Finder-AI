from JobManagers.Managers import EngineerJobsManager
from Storage.LocalStorage import LocalStorage
from Tests import TestingTools


@TestingTools.timer
def run():
    LocalStorage().clear_database()
    manager = EngineerJobsManager()
    storage = manager.storage
    jobs = manager.get_jobs()
    storage.store_jobs(jobs)
    retrieved_jobs = storage.get_jobs_from_database()
    for job in retrieved_jobs:
        print(job.get_title())
    print('Total number of jobs: ' + str(len(jobs)))