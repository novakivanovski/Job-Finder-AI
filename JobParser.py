from nltk.tokenize import word_tokenize
import logging
from Helpers import Helpers
from Job import JobMetadata
import MultiThreader


class JobParser:
    def __init__(self, file_path):
        self.keywords = []
        self.helpers = Helpers()
        self.MultiThreader = MultiThreader.MultiThreader()
        if file_path:
            keywords_file = open(file_path)
            for line in keywords_file:
                line = line.strip()
                self.keywords.append(line.lower())
            keywords_file.close()

    @staticmethod
    def get_metadata_from_page_soup(page_soup, base_url=''):
        metadata = []
        for job_entry in page_soup.find_all(class_="jobrow"):
            job_data = []
            link = base_url + job_entry.find(class_="jobtitle")['data-mdref']
            items = job_entry.find_all('td')
            for item in items:
                job_data.append(item.text)
                logging.debug(item.text)
            m = JobMetadata(url=link, title=job_data[0], location=job_data[1],
                            company=job_data[2], date=job_data[3])
            metadata.append(m)
        return metadata

    @staticmethod
    def remove_empty(jobs):
        for job in jobs:
            if not job.keywords:
                jobs.remove(job)
        return jobs

    @staticmethod
    def find_csharp(text):
        for i, t in enumerate(text):
            if t == '#':
                text[i-1] += text[i]

    @staticmethod
    def get_field(text, start_string, end_string):  # get a field from a string, e.g. jobId=abc
        start = text.find(start_string) + len(start_string)
        end = text.find(end_string, start)
        value = text[start:end]
        return value

    def filter_job_and_get_keywords(self, job):
        job.raw = (job.raw + ' ' + job.title).lower()
        raw_list = word_tokenize(job.raw)
        self.find_csharp(raw_list)  # fixes delimiter issue with C#
        raw_list = list(set(raw_list))  # remove duplicates
        for word in raw_list:
            if word[0] == '-' or word[0] == '•' or word[0] == '*':
                word = word[1:]
            if word in self.keywords:
                job.keywords.append(word)
