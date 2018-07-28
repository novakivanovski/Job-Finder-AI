from nltk.tokenize import word_tokenize
import os
import json


class ParseUtility:
    def __init__(self):
        self.config_path = os.path.join('Storage', 'config')
        self.keywords = self.load_keywords(self.config_path)

    @staticmethod
    def load_keywords(path):
        keywords_path = os.path.join(path, 'keywords.json')
        with open(keywords_path, 'r') as keywords_file:
            keywords = json.load(keywords_file)
        return keywords

    def update_keywords(self, jobs):
        for job in jobs:
            job_keywords = self.get_keywords(job)
            job.set_keywords(job_keywords)
        return jobs

    def get_keywords(self, job):
        raw_text = job.get_plaintext() + ' ' + job.get_title()
        unique_text_list = word_tokenize(raw_text)
        job_keywords = self.extract_keywords(unique_text_list)
        return job_keywords

    def extract_keywords(self, text_list):
        job_keywords = []
        for word in text_list:
            if word in self.keywords:
                job_keywords.append(word)
        return job_keywords

    @staticmethod
    def remove_and_get_empty(jobs):
        empty_jobs = []
        override_disabled = False  # for testing - to not remove the entire list of jobs
        for job in jobs:
            job_keywords = job.get_keywords()
            if not job_keywords and override_disabled:
                jobs.remove(job)
                empty_jobs.append(job)
        return empty_jobs

    @staticmethod
    def get_value_between_strings(text, start_string, end_string):
        start = text.find(start_string) + len(start_string)
        end = text.find(end_string, start)
        value = text[start:end]
        return value

    @staticmethod
    def tokenize(raw_text):
            text = raw_text.lower()
            text_list = word_tokenize(text)
            ParseUtility.csharp_workaround(text_list)
            unique_text = ParseUtility.remove_duplicates(text_list)
            return unique_text

    @staticmethod
    def csharp_workaround(text_list):
        for i, t in enumerate(text_list):
            if t == '#':
                text_list[i-1] += text_list[i]

    @staticmethod
    def remove_duplicates(text_list):
        return list(set(text_list))

    @staticmethod
    def remove_bullets(text_list):
        for word in text_list:
            if ParseUtility.starts_with_bullet(word):
                ParseUtility.remove_starting_bullet(word)
            return text_list

    @staticmethod
    def starts_with_bullet(word):
        return word[0] == '-' or word[0] == '•' or word[0] == '*'

    @staticmethod
    def remove_starting_bullet(word):
        word = word[1:]
        return word







