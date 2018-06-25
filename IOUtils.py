import os
from Job import Job
import requests
from bs4 import BeautifulSoup
import logging
from html.parser import HTMLParser
from nltk.tokenize import word_tokenize
from time import sleep


def get_html_from_url(url):
    html_text = ''
    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        html_text = response.text
    except IOError as e:
        logging.error('Request for ' + url + ' failed with exception: ' + e)
    return html_text

def get_soup_from_url(url):
    html_text = get_html_from_url(url)
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup


def purge_directory(directory):
    if os.path.exists(directory):
        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            
def create_directory(directory):
        if not os.path.exists(directory):
                os.makedirs(directory)

def get_start_index(directory):
    int_list = []
    try:
        for file in os.listdir(directory):
            i = int (file[:-4])
            int_list.append(i)
        max_value = max(int_list)
        return (max_value + 1)
    except:
        return 0

def write_jobs(jobs, pass_dir, fail_dir):
    start_pass = get_start_index(pass_dir)
    start_fail = get_start_index(fail_dir)
    
    for i, job in enumerate(jobs):
        if job.passed:
            file_name = str(start_pass + i) + '.txt'
            file_dir = os.path.join(pass_dir, file_name)
        else:
            file_name = str(start_fail + i) + '.txt'
            file_dir = os.path.join(fail_dir, file_name)
        file = open(file_dir, 'w', encoding='utf-8')
        file.write(job.title + '\n')
        for keyword in job.keywords:
            file.write(keyword + ", ")
        file.write('\n')
        file.write(job.url + '\n')
        file.write(job.location + '\n')
        file.write(job.company + '\n')
        file.write(job.date + '\n')
        file.write ('\n\n')
        raw_txt = word_tokenize(job.raw)
        for i, word in enumerate(raw_txt):
            file.write(word + ' ')
            if (i % 25) == 0:
                file.write('\n')
        file.close()

def get_jobs(directory, passed, f):
    jobs = []
    for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            file = open(file_path, 'r', encoding='utf-8')
            keywords_text = file.readlines()[1]
            keywords = word_tokenize(keywords_text)
            f.find_csharp(keywords)
            keywords = list(set(keywords))
            if len(keywords):
                keywords.remove(',')
            j = Job()
            j.keywords = keywords
            j.passed = passed
            jobs.append(j)
    return jobs


