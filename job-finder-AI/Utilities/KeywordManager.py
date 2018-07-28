import os
from DataStructures.Keyword import Keyword
from Storage.LocalStorage import LocalStorage


class KeywordManager:
    def __init__(self):
        self.config_path = os.path.join('Storage', 'config')
        self.keywords = self.load_keywords()
        self.totals = self.load_totals()

    def load_keywords(self):
        keywords = []
        keywords_path = os.path.join(self.config_path, 'keyword_data.json')
        keyword_map = LocalStorage.get_json_data(keywords_path)
        for word, count in keyword_map.items():
            k = Keyword(word, count["passed"], count["failed"])
            keywords.append(k)
        return keywords

    def load_totals(self):
        totals_path = os.path.join(self.config_path, 'totals.json')
        totals = LocalStorage.get_json_data(totals_path)
        return totals

    def save_data(self, jobs_passed, jobs_failed, keywords_passed, keywords_failed):
        self.save_keywords()
        self.save_totals(jobs_passed, jobs_failed, keywords_passed, keywords_failed)

    def save_keywords(self):
        keywords_path = os.path.join(self.config_path, 'keyword_data.json')
        json_data = self.get_keywords_as_json()
        LocalStorage.store_json_data(keywords_path, json_data)

    def save_totals(self, jobs_passed, jobs_failed, keywords_passed, keywords_failed):
        self.totals['jobs']['passed'] = jobs_passed
        self.totals['jobs']['failed'] = jobs_failed
        self.totals['keywords']['passed'] = keywords_passed
        self.totals['keywords']['failed'] = keywords_failed
        totals_path = os.path.join(self.config_path, 'totals.json')
        LocalStorage.store_json_data(totals_path, self.totals)

    def get_keywords_as_json(self):
        json_data = []
        for keyword in self.keywords:
            keyword_json = keyword.get_json_encoding()
            json_data.append(keyword_json)
        return json_data

    def clear_keyword_probabilities(self):
        for keyword in self.keywords:
            keyword.clear_data()
        self.save_keywords()

    def get_keywords(self):
        return self.keywords

    def get_total_jobs_passed(self):
        return self.totals['jobs']['passed']

    def get_total_jobs_failed(self):
        return self.totals['jobs']['failed']

    def get_total_jobs(self):
        return self.get_total_jobs_passed() + self.get_total_jobs_failed()

    def get_total_keywords_passed(self):
        return self.totals['keywords']['passed']

    def get_total_keywords_failed(self):
        return self.totals['keywords']['failed']

    def set_total_jobs_passed(self, total):
        self.totals['jobs']['passed'] = total

    def set_total_jobs_failed(self, total):
        self.totals['jobs']['failed'] = total

    def set_total_keywords_passed(self, total):
        self.totals['keywords']['passed'] = total

    def set_total_keywords_failed(self, total):
        self.totals['keywords']['failed'] = total

    def set_keyword_probabilities(self):
        number_keywords_passed = 0
        number_keywords_failed = 0
        for keyword in self.keywords:
            number_keywords_passed += keyword.get_pass_count()
            number_keywords_failed += keyword.get_fail_count()

        for keyword in self.keywords:
            keyword.set_pass_probability(number_keywords_passed)
            keyword.set_fail_probability(number_keywords_failed)


