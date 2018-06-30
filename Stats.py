# P(A)*P(B|A) > P(¬A)*P(B|¬A)
from math import pow


class Stats:
    def __init__(self, keywords):
        self.pA = 0
        self.pNotA = 1
        self.nPass = 0
        self.nFail = 0
        self.total = 0
        self.nWords = 0
        self.keyword_dict = {}
        for word in keywords:
            self.keyword_dict[word] = [0, 0]

    @staticmethod
    def get_keyword_prob(job, keyword):
        pass_probability = 0
        fail_probability = 0
        if job.passed and keyword in job.keywords:
            pass_probability += 1
            
        elif not job.passed and keyword in job.keywords:
            fail_probability += 1
            
        prob = {'passed': pass_probability, 'failed': fail_probability}
        return prob

    def clear_training_data(self):
        self.pA = 0
        self.pNotA = 1
        self.nPass = 0
        self.nFail = 0
        self.total = 0
        self.nWords = 0
        for word in self.keyword_dict:
            self.keyword_dict[word] = [0, 0]
    
    def train(self, jobs):
        pass_count = 0
        fail_count = 0

        for job in jobs:
            self.total = self.total + 1
            self.nWords += len(job.keywords)
            
            if job.passed:
                pass_count = pass_count + 1
                self.nPass = self.nPass + len(job.keywords)
            else:
                fail_count = fail_count + 1
                self.nFail = self.nFail + len(job.keywords)

            for keyword in self.keyword_dict:
                prob = self.get_keyword_prob(job, keyword)
                self.keyword_dict[keyword][0] += prob['passed']
                self.keyword_dict[keyword][1] += prob['failed']

        for keyword in self.keyword_dict:  # divide by total words to get prob
            if self.nPass > 0:
                self.keyword_dict[keyword][0] /= self.nPass
            if self.nFail > 0:
                self.keyword_dict[keyword][1] /= self.nFail

        if self.total > 0:
            self.pA = pass_count/self.total
            self.pNotA = fail_count/self.total

    def classify(self, job):
        pass_probability = 1
        fail_probability = 1
        alpha = pow(10, -55)  # laplace smoothing factor 1e-55
        for keyword in self.keyword_dict:
            if keyword in job.keywords:
                pass_probability *= self.keyword_dict[keyword][0]
                fail_probability *= self.keyword_dict[keyword][1]
        pass_probability *= self.pA
        fail_probability *= self.pNotA
        pass_probability += alpha
        fail_probability += alpha
        return pass_probability/fail_probability > 1

