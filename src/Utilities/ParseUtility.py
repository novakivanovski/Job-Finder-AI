from nltk.tokenize import word_tokenize
from Storage.LocalStorage import LocalStorage


class ParseUtility:
    def __init__(self):
        self.keyword_names = LocalStorage.get_keyword_names()

    def update_keywords(self, jobs):
        for job in jobs:
            keyword_names = self.extract_keyword_names(job)
            job.set_keyword_names(keyword_names)
        return jobs

    def extract_keyword_names(self, job):
        text = job.get_plaintext() + ' ' + job.get_title()
        unique_text_list = self.tokenize(text)
        job_keyword_names = self.in_both(unique_text_list, self.keyword_names)
        return job_keyword_names

    @staticmethod
    def in_both(list_a, list_b):
        result = set(list_a) & set(list_b)
        return list(result)

    @staticmethod
    def pop_empty(jobs):
        empty_jobs = []
        override_enabled = True  # for testing - to not remove all jobs
        for job in jobs:
            job_keywords = job.get_keyword_names()
            if not job_keywords and not override_enabled:
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







