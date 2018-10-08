import argparse
from JobManager import JobManager
from Crawlers import EngineerJobsCrawler, IndeedCrawler
from DataStructures.Listers import EngineerJobsLister, IndeedLister
from Utilities import TextFormatter
from Utilities.Stats import Stats


class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Command line interface for job searcher AI.')
        parser.add_argument('-clear', help='Clear local job cache and database.', action='store_true')
        parser.add_argument('-crawl', help='Crawl job postings and save them locally.', action='store_true')
        parser.add_argument('-train', help='Train the AI by classifying jobs as passed/failed.', action='store_true')
        parser.add_argument('-classify', help='Show results of classification applied to cache.', action='store_true')
        parser.add_argument('-time', help='Specify how many days to crawl')
        parser.add_argument('-store', help='Store jobs in database.', action='store_true')
        args = parser.parse_args()
        self.args_to_values = vars(args)
        self.stats = Stats()
        self.job_manager = JobManager()
        self.storage = self.job_manager.storage
        self.args_to_functions = {'clear': self.clear, 'crawl': self.crawl,
                                  'train': self.train, 'classify': self.classify}
        self.execute()

    def execute(self):
        for argument in self.args_to_functions:
            argument_provided = self.args_to_values[argument]
            if argument_provided:
                run_function = self.args_to_functions[argument]
                run_function()

    def classify(self):
        print('Classifying jobs...')
        jobs = self.storage.get_jobs_from_cache()
        for job in jobs:
            score = self.stats.classify(job)
            job.set_score(score)
            if score > 1.0:
                self.print_classify_info(job)

    def crawl(self):
        print('Crawling job postings...')
        time = int(self.args_to_values['time']) if self.args_to_values['time'] else 1
        print('Number of days to crawl: ' + str(time))
        self.job_manager.crawler = IndeedCrawler.IndeedCrawler(time)
        self.job_manager.lister = IndeedLister.IndeedLister(self.job_manager.get_last_job_id())
        jobs = self.job_manager.get_jobs()
        print('Saving ' + str(len(jobs)) + ' jobs...')
        self.storage.store_jobs(jobs)

    def train(self):
        print('Starting training session...')
        print('Enter exit to quit.')
        jobs = self.storage.get_jobs_from_database()
        num_jobs = len(jobs)
        current_job = 0
        exit_condition = False
        print('Number of jobs ' + str(num_jobs))
        while not exit_condition:
            job = jobs[current_job]
            self.print_training_info(job)
            user_exit = self.process_job_passed(job)
            exit_condition = user_exit or current_job == num_jobs - 1
            current_job += 1
        self.stats.train(jobs)

    @staticmethod
    def print_training_info(job):
        job_description = TextFormatter.format_job_description(job.get_plaintext())
        job_title = TextFormatter.format_job_title(job.get_title())
        job_keywords = TextFormatter.format_job_keywords(job.get_keyword_names())
        TextFormatter.multi_print(job_title, job_description, job_keywords)

    @staticmethod
    def print_classify_info(job):
        job_title = TextFormatter.format_job_title(job.get_title())
        job_keywords = TextFormatter.format_job_keywords(job.get_keyword_names())
        job_score = TextFormatter.format_job_score(job.get_score())
        TextFormatter.multi_print(job_title, job_keywords, job_score)

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

    def clear(self):
        print('Clearing local cache and database...')
        self.storage.clear_cache()
        self.storage.clear_database()



