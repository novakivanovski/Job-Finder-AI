import argparse
from JobManager import JobManager
from Storage.LocalStorage import LocalStorage
from Crawlers import EngineerJobsCrawler
from DataStructures.Listers import EngineerJobsLister
from Utilities.Stats import Stats


class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Command line interface for job searcher AI.')
        parser.add_argument('-clean', help='Clean local job cache.', action='store_true')
        parser.add_argument('-crawl', help='Crawl job postings and save them locally.', action='store_true')
        parser.add_argument('-train', help='Train the AI by classifying jobs as passed/failed.', action='store_true')
        args = parser.parse_args()
        self.args_to_values = vars(args)
        self.storage = LocalStorage()
        self.args_to_functions = {'crawl': self.crawl, 'train': self.train, 'clean': self.clean}
        self.execute()

    def execute(self):
        for argument in self.args_to_values:
            argument_provided = self.args_to_values[argument]
            if argument_provided:
                run_function = self.args_to_functions[argument]
                run_function()

    def crawl(self):
        print('Crawling job postings...')
        crawler = EngineerJobsCrawler.EngineerJobsCrawler()
        lister = EngineerJobsLister.EngineerJobsLister()
        manager = JobManager(crawler, lister)
        jobs = manager.get_jobs()
        self.storage.store_jobs(jobs)

    def train(self):
        print('Starting training session...')
        print('Enter exit to quit.')
        jobs = self.storage.retrieve_jobs()
        for job in jobs:
            print(job.get_title())
            print(job.get_plaintext())
            job_passed = input('Job passed? y/n. ')
            if job_passed == 'exit':
                exit()
            job.set_passed(job_passed)
        stats = Stats()
        stats.train(jobs)

    def clean(self):
        print('Clearing local cache...')
        self.storage.clear_cache()


