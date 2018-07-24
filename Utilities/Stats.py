# P(A)*P(B|A) > P(¬A)*P(B|¬A)
from math import pow
import os
import json
from DataStructures.Keyword import Keyword


class Stats:
    def __init__(self):
        self.keywords_path = os.path.join('config', 'keywords.json')
        self.keywords = self.load_keywords()
        self.probability_pass = 0
        self.probability_fail = 1
        self.number_passed = 0
        self.number_failed = 0
        self.number_total = 0
        self.number_words = 0

    def load_keywords(self):
        keywords = []
        with open(self.keywords_path, 'r') as json_file:
            keyword_map = json.loads(json_file.read())
        for word, word_probability in keyword_map.items():
            k = Keyword(word, word_probability["passed"], word_probability["failed"])
            keywords.append(k)
        return keywords

    @staticmethod
    def keyword_passed(job, keyword):
        return int(job.passed and keyword in job.keyword)

    @staticmethod
    def keyword_failed(job, keyword):
        return int(not job.passed and keyword in job.keywords)

    def clear_training_data(self):
        self.probability_pass = 0
        self.probability_fail = 1
        self.number_passed = 0
        self.number_failed = 0
        self.number_total = 0
        self.number_words = 0
        for keyword in self.keywords:
            keyword.clear_probabilities()
    
    def train(self, jobs):
        pass_count = 0
        fail_count = 0

        for job in jobs:
            self.number_total = self.number_total + 1
            self.number_words += len(job.keywords)
            
            if job.passed:
                pass_count = pass_count + 1
                self.number_passed = self.number_passed + len(job.keywords)
            else:
                fail_count = fail_count + 1
                self.number_failed = self.number_failed + len(job.keywords)

            for keyword in self.keywords:
                keyword.pass_probability += self.keyword_passed(job, keyword)
                keyword.fail_probability += self.keyword_failed(job, keyword)

        for keyword in self.keywords:  # divide by number_total words to get prob
            if self.number_passed > 0:
                keyword.pass_probability /= self.number_passed
            if self.number_failed > 0:
                keyword.fail_probability /= self.number_failed

        if self.number_total > 0:
            self.probability_pass = pass_count / self.number_total
            self.probability_fail = fail_count / self.number_total

    def classify(self, job):
        pass_probability = 1
        fail_probability = 1
        alpha = pow(10, -55)  # laplace smoothing factor 1e-55
        for keyword in self.keywords:
            if keyword.get_name() in job.keywords:
                pass_probability *= keyword.get_pass_probability()
                fail_probability *= keyword.get_fail_probability()
        pass_probability *= self.probability_pass
        fail_probability *= self.probability_fail
        pass_probability += alpha
        fail_probability += alpha
        return pass_probability/fail_probability > 1

