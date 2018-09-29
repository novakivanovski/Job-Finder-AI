import argparse
from JobManager import JobManager
from Storage.LocalStorage import LocalStorage
from Crawlers import EngineerJobsCrawler
from DataStructures.Listers import EngineerJobsLister
from Utilities.Stats import Stats
from Utilities import TextFormatter
from Utilities.KeywordManager import KeywordManager

class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Command line interface for job searcher AI.')
        parser.add_argument('-clean', help='Clean local job cache.', action='store_true')
        parser.add_argument('-crawl', help='Crawl job postings and save them locally.', action='store_true')
        parser.add_argument('-train', help='Train the AI by classifying jobs as passed/failed.', action='store_true')
        parser.add_argument('classify', help='Show results of classification applied to cache.', action='store_true')
        args = parser.parse_args()
        self.args_to_values = vars(args)
        self.storage = LocalStorage()
        self.args_to_functions = {'crawl': self.crawl, 'train': self.train, 'clean': self.clean, 'classify': self.classify}
        self.execute()
        self.bootstrap()

    def execute(self):
        for argument in self.args_to_values:
            argument_provided = self.args_to_values[argument]
            if argument_provided:
                run_function = self.args_to_functions[argument]
                run_function()

    def bootstrap(self):
        kw_manager = KeywordManager()


    def classify(self):
        print('Classifying jobs...')
        jobs = self.storage.retrieve_jobs()
        for job in jobs:
            print(job.passed)

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
        num_jobs = len(jobs)
        current_job = 0
        exit_condition = False
        while not exit_condition:
            job = jobs[current_job]
            self.print_job_training_information(job)
            self.print_job_training_information(job)
            user_exit = self.process_job_passed(job)
            exit_condition = user_exit or current_job == num_jobs - 1
            current_job += 1
        self.storage.store_jobs(jobs)

    def print_job_training_information(self, job):
        job_description = job.get_plaintext()
        job_title = job.get_title()
        job_keywords = job.extract_keyword_names()
        self.print_job_title(job_title)
        self.print_job_description(job_description)
        self.print_job_keywords(job_keywords)

    @staticmethod
    def print_job_description(job_description):
        header_text = TextFormatter.format_header('Job Description')
        description_text = TextFormatter.reformat_text(job_description)
        print(header_text)
        print(description_text)

    @staticmethod
    def print_job_title(job_title):
        header_text = 'Job Title: ' + job_title
        header_text = TextFormatter.format_header(header_text)
        print(header_text)

    @staticmethod
    def print_job_keywords(job_keywords):
        header_text = 'Job Keywords: ' + str(job_keywords)
        header_text = TextFormatter.format_header(header_text)
        print(header_text)

    @staticmethod
    def process_job_passed(job):
        user_exit = False
        job_passed = input('Job passed? y/n ')
        if job_passed == 'y':
            job.set_passed(True)
        elif job_passed == 'n':
            job.set_passed(False)
        else:
            print('Exiting...')
            user_exit = True
        return user_exit

    def clean(self):
        print('Clearing local cache...')
        self.storage.clear_cache()


