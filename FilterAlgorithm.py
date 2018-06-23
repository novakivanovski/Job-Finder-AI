import requests
from math import ceil
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from JobObject import JobObject
from time import time
import json
from Helpers import Helpers
from threading import Thread

class FilterAlgorithm():

    def remove_empty(self, jobs):
        for job in jobs:
            if not job.keywords:
                jobs.remove(job)

    def __init__(self, file_path):
        
        self.keywords = []
        self.helpers = Helpers()
        keywords_file = open(file_path)

        for line in keywords_file:
            line = line.strip()
            self.keywords.append(line.lower())
            
        keywords_file.close()

    def find_csharp(self, text):
        for i, t in enumerate(text):
            if t == '#':
                text[i-1] += text[i]

    def multi_thread(self, job, q):
        self.helpers.get_raw(job)
        q.put(True)
        job.raw = (job.raw + ' ' + job.title).lower()
        raw_list = word_tokenize(job.raw)
        self.find_csharp(raw_list) # fixes delimiter issue with C# 
        raw_list = list(set(raw_list)) # remove duplicates
        for word in raw_list:
            if word[0] == '-' or word[0] == '•'  or word[0] == '*':
                word = word[1:]
            if word in self.keywords:
                job.keywords.append(word)

        
    def extract(self, jobs, q):
        threads = []
        start = time()
        
        for job in jobs:
            t = Thread(target=self.multi_thread, args=(job, q))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
            
        self.remove_empty(jobs)
        
     
        
