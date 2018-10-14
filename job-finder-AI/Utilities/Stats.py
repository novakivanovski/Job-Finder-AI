# P(A)*P(B|A) > P(¬A)*P(B|¬A)
from math import pow
from Utilities.ApplicationExceptions import StatsError
from Utilities.StatsData import StatsData


class Stats:
    def __init__(self):
        self.stats_data = StatsData()

    @staticmethod
    def keyword_passed(job, keyword):
        return int(job.passed and keyword.name in job.keyword_names)

    @staticmethod
    def keyword_failed(job, keyword):
        return int(not job.passed and keyword.name in job.keyword_names)

    def train(self, jobs):
        keywords = self.stats_data.get_keywords()
        number_jobs_passed = self.stats_data.get_total_jobs_passed()
        number_jobs_failed = self.stats_data.get_total_jobs_failed()

        for job in jobs:
            if job.passed:
                number_jobs_passed += 1
            else:
                number_jobs_failed += 1

            for keyword in keywords:
                keyword.pass_count += self.keyword_passed(job, keyword)
                keyword.fail_count += self.keyword_failed(job, keyword)

        if not number_jobs_failed or not number_jobs_passed:
            raise StatsError('Insufficient training data supplied.')
        self.stats_data.update_data(keywords, number_jobs_passed, number_jobs_failed)

    def clear_data(self):
        self.stats_data.clear_data()

    def classify(self, job):
        keywords = self.stats_data.get_keywords()
        job_pass_probability = self.stats_data.get_job_pass_probability()
        job_fail_probability = self.stats_data.get_job_fail_probability()
        pass_probability = 1
        fail_probability = 1
        alpha = pow(10, -50)  # laplace smoothing factor 1e-50
        for keyword in keywords:
            if keyword.get_name() in job.keyword_names:
                pass_probability *= keyword.get_pass_probability()
                fail_probability *= keyword.get_fail_probability()
        pass_probability *= job_pass_probability
        fail_probability *= job_fail_probability
        pass_probability += alpha
        fail_probability += alpha
        return pass_probability/fail_probability

