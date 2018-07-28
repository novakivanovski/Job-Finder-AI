# P(A)*P(B|A) > P(¬A)*P(B|¬A)
from math import pow
from Utilities.ApplicationExceptions import StatsError
from Utilities.KeywordManager import KeywordManager


class Stats:
    def __init__(self):
        self.keyword_manager = KeywordManager()
        self.keywords = self.keyword_manager.get_keywords()
        self.number_keywords_passed = 0
        self.number_keywords_failed = 0
        self.number_jobs = 0
        self.number_jobs_passed = 0
        self.number_jobs_failed = 0
        self.job_pass_probability = 0
        self.job_fail_probability = 0

    def load_training_data(self):
        self.keyword_manager.set_keyword_probabilities()
        self.number_jobs_passed = self.keyword_manager.get_total_jobs_passed()
        self.number_jobs_failed = self.keyword_manager.get_total_jobs_failed()
        self.number_jobs = self.number_jobs_passed + self.number_jobs_failed
        self.job_pass_probability = self.number_jobs_passed / self.number_jobs
        self.job_fail_probability = self.number_jobs_failed / self.number_jobs
        self.number_keywords_passed = self.keyword_manager.get_total_keywords_passed()
        self.number_keywords_passed = self.keyword_manager.get_total_keywords_failed()

    def save_training_data(self):
        self.keyword_manager.save_data(self.number_keywords_passed, self.number_jobs_failed,
                                       self.number_keywords_passed, self.number_keywords_failed)

    def clear_training_data(self):
        self.keyword_manager.clear_keyword_probabilities()
        self.number_keywords_passed = 0
        self.number_keywords_failed = 0
        self.number_jobs = 0
        self.number_jobs_passed = 0
        self.number_jobs_failed = 0
        self.job_pass_probability = 0
        self.job_fail_probability = 0

    @staticmethod
    def keyword_passed(job, keyword):
        return int(job.passed and keyword in job.keyword)

    @staticmethod
    def keyword_failed(job, keyword):
        return int(not job.passed and keyword in job.keywords)

    def train(self, jobs):
        self.clear_training_data()

        for job in jobs:
            self.number_jobs += 1
            number_keywords = len(job.keywords)
            
            if job.passed:
                self.number_jobs_passed += 1
                self.number_keywords_passed += number_keywords
            else:
                self.number_jobs_failed += 1
                self.number_keywords_failed += number_keywords

            for keyword in self.keywords:
                keyword.pass_count += self.keyword_passed(job, keyword)
                keyword.fail_count += self.keyword_failed(job, keyword)

        for keyword in self.keywords:  # divide by number_total words to get prob
            if self.number_keywords_passed > 0:
                keyword.set_pass_probability(self.number_keywords_passed)
            if self.number_keywords_failed > 0:
                keyword.set_fail_probability(self.number_keywords_failed)

        if not self.number_jobs:
            raise StatsError('No training data supplied.')

        self.job_pass_probability = self.number_jobs_passed / self.number_jobs
        self.job_fail_probability = self.number_jobs_failed / self.number_jobs

        self.save_training_data()

    def classify(self, job):
        pass_probability = 1
        fail_probability = 1
        alpha = pow(10, -55)  # laplace smoothing factor 1e-55
        for keyword in self.keywords:
            if keyword.get_name() in job.keywords:
                pass_probability *= keyword.get_pass_probability()
                fail_probability *= keyword.get_fail_probability()
        pass_probability *= self.job_pass_probability
        fail_probability *= self.job_fail_probability
        pass_probability += alpha
        fail_probability += alpha
        return pass_probability/fail_probability > 1

