# P(A)*P(B|A) > P(¬A)*P(B|¬A)
from math import pow
from Utilities.ApplicationExceptions import StatsError
from Utilities.KeywordManager import KeywordManager


class Stats:
    def __init__(self):
        self.keyword_manager = KeywordManager()
        self.keywords = self.keyword_manager.get_keywords()
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

    def save_training_data(self):
        self.keyword_manager.save_data(self.number_jobs_passed, self.number_jobs_failed)

    def clear_training_data(self):
        self.keyword_manager.clear_keyword_probabilities()
        self.number_jobs = 0
        self.number_jobs_passed = 0
        self.number_jobs_failed = 0
        self.job_pass_probability = 0
        self.job_fail_probability = 0

    @staticmethod
    def keyword_passed(job, keyword):
        return int(job.passed and keyword.name in job.keyword_names)

    @staticmethod
    def keyword_failed(job, keyword):
        return int(not job.passed and keyword.name in job.keyword_names)

    def train(self, jobs):
        self.clear_training_data()

        for job in jobs:
            self.number_jobs += 1
            if job.passed:
                self.number_jobs_passed += 1
            else:
                self.number_jobs_failed += 1

            for keyword in self.keywords:
                keyword.pass_count += self.keyword_passed(job, keyword)
                keyword.fail_count += self.keyword_failed(job, keyword)

        if not self.number_jobs or not self.number_jobs_failed or not self.number_jobs_passed:
            raise StatsError('Insufficient training data supplied.')

        for keyword in self.keywords:
            keyword.set_pass_probability(self.number_jobs_passed)
            keyword.set_fail_probability(self.number_jobs_failed)

        self.job_pass_probability = self.number_jobs_passed / self.number_jobs
        self.job_fail_probability = self.number_jobs_failed / self.number_jobs
        self.save_training_data()

    def classify(self, job):
        pass_probability = 1
        fail_probability = 1
        alpha = pow(10, -55)  # laplace smoothing factor 1e-55
        for keyword in self.keywords:
            if keyword.get_name() in job.keyword_names:
                pass_probability *= keyword.get_pass_probability()
                fail_probability *= keyword.get_fail_probability()
        pass_probability *= self.job_pass_probability
        fail_probability *= self.job_fail_probability
        pass_probability += alpha
        fail_probability += alpha
        return pass_probability/fail_probability

