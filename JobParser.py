from nltk.tokenize import word_tokenize
import logging
from Job import JobMetadata, JobDescription
import MultiThreader


class JobParser:
    def __init__(self, file_path):
        self.keywords = []
        self.MultiThreader = MultiThreader.MultiThreader()
        if file_path:
            keywords_file = open(file_path)
            for line in keywords_file:
                line = line.strip()
                self.keywords.append(line.lower())
            keywords_file.close()

    @staticmethod
    def get_metadata(page_soups):
        metadata = []
        for soup in page_soups:
            page_metadata = JobParser.get_page_metadata_from_soup(soup)
            metadata += page_metadata
        return metadata

    @staticmethod
    def get_page_metadata_from_soup(page_soup, base_url='https://www.engineerjobs.com'):
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
    def get_descriptions(description_soups):
        descriptions = []
        for soup in description_soups:
            description = JobDescription(soup)
            descriptions.append(description)
        return descriptions


    @staticmethod
    def remove_empty(jobs):
        for job in jobs:
            if not job.keywords:
                jobs.remove(job)
        return jobs

    @staticmethod
    def csharp_workaround(text_list):
        for i, t in enumerate(text_list):
            if t == '#':
                text_list[i-1] += text_list[i]

    @staticmethod
    def get_value_between_strings(text, start_string, end_string):
        start = text.find(start_string) + len(start_string)
        end = text.find(end_string, start)
        value = text[start:end]
        return value

    def tokenize(self, raw_text):
        text = raw_text.lower()
        text_list = word_tokenize(text)
        self.csharp_workaround(text_list)
        unique_text = self.remove_duplicates(text_list)
        return unique_text

    @staticmethod
    def remove_duplicates(text_list):
        return list(set(text_list))

    @staticmethod
    def remove_bullets(text_list):
        for word in text_list:
            if JobParser.starts_with_bullet(word):
                JobParser.remove_starting_bullet(word)
        return text_list

    @staticmethod
    def starts_with_bullet(word):
        return word[0] == '-' or word[0] == '•' or word[0] == '*'

    @staticmethod
    def remove_starting_bullet(word):
        word = word[1:]
        return word

    def extract_keywords(self, text_list):
        keywords = []
        for word in text_list:
            if word in self.keywords:
                keywords.append(word)
        return keywords

    def get_keywords(self, job):
        raw_text = job.get_raw() + ' ' + job.get_title()
        unique_text_list = self.tokenize(raw_text)
        keywords = self.extract_keywords(unique_text_list)
        return keywords
