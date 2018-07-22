from nltk.tokenize import word_tokenize
import logging


with open('keywords.txt', 'r') as keywords_file:
    keywords_data = keywords_file.read()
    keywords = keywords_data.split('\n')

logging.debug('Imported ParsingUtilities with keywords: ' + str(keywords))


def update_keywords(jobs):
    for job in jobs:
        job_keywords = get_keywords(job)
        job.set_keywords(job_keywords)
    return jobs


def get_keywords(job):
    raw_text = job.get_plaintext() + ' ' + job.get_title()
    unique_text_list = tokenize(raw_text)
    job_keywords = extract_keywords(unique_text_list)
    return job_keywords


def extract_keywords(text_list):
    job_keywords = []
    for word in text_list:
        if word in keywords:
            job_keywords.append(word)
    return job_keywords


def remove_and_get_empty(jobs):
    pass


'''''''''
def remove_and_get_empty(jobs):
    empty_jobs = []
    for job in jobs:
        job_keywords = job.get_keywords()
        if not job_keywords:
            jobs.remove(job)
            empty_jobs.append(job)
    return empty_jobs
'''''''''

def get_value_between_strings(text, start_string, end_string):
    start = text.find(start_string) + len(start_string)
    end = text.find(end_string, start)
    value = text[start:end]
    return value


def tokenize(raw_text):
        text = raw_text.lower()
        text_list = word_tokenize(text)
        csharp_workaround(text_list)
        unique_text = remove_duplicates(text_list)
        return unique_text


def csharp_workaround(text_list):
    for i, t in enumerate(text_list):
        if t == '#':
            text_list[i-1] += text_list[i]


def remove_duplicates(text_list):
    return list(set(text_list))


def remove_bullets(text_list):
    for word in text_list:
        if starts_with_bullet(word):
            remove_starting_bullet(word)
        return text_list


def starts_with_bullet(word):
    return word[0] == '-' or word[0] == '•' or word[0] == '*'


def remove_starting_bullet(word):
    word = word[1:]
    return word







