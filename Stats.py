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
            
    def get_keyword_prob(self, job, keyword):
        passP = 0
        failP = 0
        if job.passed and keyword in job.keywords:
            passP = passP + 1
            
        elif not(job.passed) and (keyword in job.keywords):
            failP = failP + 1
            
        prob = {'passed': passP, 'failed' : failP}
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
        passCount = 0
        failCount = 0

        for job in jobs:
            self.total = self.total + 1
            self.nWords += len(job.keywords)
            
            if job.passed:
                passCount = passCount + 1
                self.nPass = self.nPass + len(job.keywords)
            else:
                failCount = failCount + 1
                self.nFail = self.nFail + len(job.keywords)

            for keyword in self.keyword_dict:
                prob = self.get_keyword_prob(job, keyword)
                self.keyword_dict[keyword][0] += prob['passed']
                self.keyword_dict[keyword][1] += prob['failed']

        for keyword in self.keyword_dict:  #divide by total words to get prob
            if self.nPass > 0:
                self.keyword_dict[keyword][0] /= self.nPass
            if self.nFail > 0:
                self.keyword_dict[keyword][1] /= self.nFail

        if (self.total > 0):
            self.pA = passCount/self.total
            self.pNotA = failCount/self.total


    def classify(self, job):
        pPass = 1
        pFail = 1
        alpha = pow(10, -55) # laplace smoothing factor 1e-55
        for keyword in self.keyword_dict:
            if keyword in job.keywords:
                pPass *= self.keyword_dict[keyword][0]
                pFail *= self.keyword_dict[keyword][1]
        pPass *= self.pA 
        pFail *= self.pNotA
        pPass += alpha
        pFail += alpha
        return (pPass/pFail > 1)
 


        
            
                
        
        
        
            
        

    
