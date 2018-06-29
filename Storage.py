import os  # put some of the IOUtils stuff here - split into networking and local IO (OS stuff)
import pickle
import logging
from nltk import word_tokenize


class Storage:
    def __init__(self, base_directory):
        self.base_dir = base_directory
        self.jobs_dir = os.path.join(base_directory, 'jobs')
        self.train_dir = os.path.join(self.jobs_dir, 'training')
        self.train_pass_dir = os.path.join(self.train_dir, 'pass')
        self.train_fail_dir = os.path.join(self.train_dir, 'fail')
        self.classify_dir = os.path.join(self.jobs_dir, 'classify')
        self.job_file_name = 'job.txt'
        self.job_object_name = 'job.pickle'

    def store_jobs(self, jobs):
        for job in jobs:
            self.store_job(job)

    def store_job(self, job):
        job_dir = os.path.join(self.jobs_dir, job.metadata.id)
        self.create_directory(job_dir)
        text_file_path = os.path.join(job_dir, self.job_file_name)
        object_file_path = os.path.join(job_dir, self.job_object_name)
        self.store_text(text_file_path, job.text)
        self.store_object(object_file_path, job)

    @staticmethod
    def store_object(file_path, obj):
        try:
            with open(file_path, 'wb') as file:
                pickle.dump(obj, file)
        except Exception as e:
            logging.error('Error while pickling: ' + str(e))

    @staticmethod
    def retrieve_object(file_path):
        obj = None
        try:
            with open(file_path, 'r') as file:
                obj = pickle.load(file)
        except Exception as e:
                logging.error('Error while retrieving object: ' + str(e))
        return obj

    @staticmethod
    def store_text(file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)
        except Exception as e:
            logging.error('Error while storing text: ' + str(e))

    @staticmethod
    def retrieve_text(file_path):
        text = ''
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            logging.error('Error while retrieving text file: ' + str(e))
        return text

    def clear_jobs(self):
        self.clear_directory(self.jobs_dir)

    @staticmethod
    def clear_directory(directory):
        if os.path.exists(directory):
            for the_file in os.listdir(directory):
                file_path = os.path.join(directory, the_file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

    @staticmethod
    def create_directory(directory):
        if not os.path.exists(directory):
                os.makedirs(directory)

    @staticmethod
    def get_start_index(directory):
        int_list = []
        max_value = 0
        try:
            for file in os.listdir(directory):
                i = int (file[:-4])
                int_list.append(i)
            max_value = max(int_list)
        except Exception as e:
            logging.error(e)
        return max_value

    def write_jobs(self, jobs, pass_dir, fail_dir):
        start_pass = self.get_start_index(pass_dir)
        start_fail = self.get_start_index(fail_dir)
    
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
            for j, word in enumerate(raw_txt):
                file.write(word + ' ')
                if (j % 25) == 0:
                    file.write('\n')
            file.close()

    @staticmethod
    def get_jobs(directory, f):
        keywords_list = []
        for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                file = open(file_path, 'r', encoding='utf-8')
                keywords_text = file.readlines()[1]
                keywords = word_tokenize(keywords_text)
                f.find_csharp(keywords)
                keywords = list(set(keywords))
                if len(keywords):
                    keywords.remove(',')
                keywords_list.append(keywords)
        return keywords_list