import argparse
from Crawlers import IndeedCrawler
from Listers import IndeedLister
from Utilities import TextFormatter
from Utilities.Stats import Stats
import logging
from Utilities import Loader
from UI import InputProcessors


class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Command line interface for job searcher AI.')
        parser.add_argument('-clear', help='Clear local job cache and database.', action='store_true')
        parser.add_argument('-crawl', help='Crawl job postings and save them locally.', action='store_true')
        parser.add_argument('-train', help='Train the AI by classifying jobs as passed/failed.', action='store_true')
        parser.add_argument('-classify', help='Show results of classification applied to cache.', action='store_true')
        parser.add_argument('-time', help='Specify how many days to crawl')
        parser.add_argument('-store', help='Store jobs in database.', action='store_true')
        parser.add_argument('-site', help='Specify site: indeed or engineerjobs currently supported.')
        args = parser.parse_args()
        self.args_to_values = vars(args)
        self.stats = Stats()
        self.job_manager = self.get_manager()
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
        jobs = self.storage.get_jobs_from_database()
        for job in jobs:
            score = self.stats.classify(job)
            job.set_score(score)
            self.print_classify_info(job)

    def crawl(self):
        print('Crawling job postings...')
        time = int(self.args_to_values['time']) if self.args_to_values['time'] else 1
        print('Number of days to crawl: ' + str(time))
        self.job_manager.crawler = IndeedCrawler.IndeedCrawler(time)
        self.job_manager.lister = IndeedLister.IndeedLister(self.job_manager.get_last_job_id())
        jobs = self.job_manager.get_jobs()
        print('Saving ' + str(len(jobs)) + ' jobs...')
        self.storage.store_jobs_in_database(jobs)

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

    def get_manager(self):
        site = self.args_to_values['site']
        site_to_manager = {'engineerjobs': 'EngineerJobsManager',
                           'indeed': 'IndeedManager',
                           'linkedin': 'LinkedInManager'}
        manager_name = 'IndeedManager' if site not in site_to_manager else site_to_manager[site]
        print('Creating instance of ' + manager_name)
        return Loader.load_class('JobManagers', 'Managers', manager_name)

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
        job_url = TextFormatter.format_job_url(job.get_posting_url())
        if job.score > 1.0:
            TextFormatter.multi_print(job_title, job_keywords, job_score, job_url)
        logging.info(job_title)
        logging.info(job_keywords)
        logging.info(job_score)
        logging.info(job_url)

    def process_job_passed(self, job):
        user_input = input('Job passed? y/n ').lower()
        input_processor = InputProcessors.get_processor(user_input, job, self.process_job_passed)
        user_exit = input_processor.process()
        self.storage.update_job_in_database(job)
        return user_exit

    def clear(self):
        print('Clearing local cache and database...')
        self.storage.clear_cache()
        self.storage.clear_database()



