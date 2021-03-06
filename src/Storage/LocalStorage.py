import os
import pickle
import logging
from enum import Enum
import json
from Utilities.ApplicationExceptions import storage_error
from Storage.JobDatabase import JobDatabase
import zipfile
from Utilities import TextFormatter


class Path(Enum):
    FILE = 0
    FOLDER = 1
    ALL = 2


class LocalStorage:
    def __init__(self):
        self.base_dir = os.path.join('Storage')
        self.cache_dir = os.path.join(self.base_dir, 'cache')
        self.jobs_dir = os.path.join(self.cache_dir, 'jobs')
        self.listings_dir = os.path.join(self.cache_dir, 'listings')
        self.config_dir = os.path.join(self.base_dir, 'config')
        self.backup_dir = os.path.join(self.base_dir, 'backup')
        self.database_path = os.path.join(self.config_dir, 'database.db')
        self.job_file_name = 'job.txt'
        self.job_object_name = 'job.pickle'
        self.database = JobDatabase()

    @storage_error()
    def store_jobs(self, jobs):
        self.clear_cache()
        self.create_directory(self.jobs_dir)
        self.create_directory(self.listings_dir)
        self.store_jobs_in_cache(jobs)
        self.store_jobs_in_database(jobs)

    def store_jobs_in_cache(self, jobs):
        for job in jobs:
            job_id = str(job.get_id())
            job_txt = job_id + '.txt'
            job_pickle = job_id + '.pickle'
            listing_file_path = os.path.join(self.listings_dir, job_txt)
            job_pickle_path = os.path.join(self.jobs_dir, job_pickle)
            self.store_job_listing_data(listing_file_path, job)
            self.store_object(job_pickle_path, job)

    @staticmethod
    def store_object(file_path, obj):
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)

    def get_jobs_from_database(self):
        return self.database.get_jobs()

    @storage_error()
    def get_jobs_from_cache(self):
        pickle_paths = self.get_pickles_in_folder(self.jobs_dir)
        jobs = []
        for pickle_path in pickle_paths:
            job = self.retrieve_object(pickle_path)
            jobs.append(job)
        return jobs

    def get_pickles_in_folder(self, folder):
        files = self.get_files_from_path(folder)
        pickles = self.get_files_with_extension(files, extension='.pickle')
        return pickles

    @staticmethod
    def get_files_with_extension(files_in, extension=''):
        files_out = []
        for file in files_in:
            if file.endswith(extension):
                files_out.append(file)
        return files_out

    @staticmethod
    def retrieve_object(file_path):
        with open(file_path, 'rb') as file:
            obj = pickle.load(file)
        return obj

    @staticmethod
    def store_job_listing_data(file_path, job):
        with open(file_path, 'w', encoding='utf-8') as file:
            listing = job.listing
            file.write('Job title: ' + listing.title + '\n')
            file.write('Posting date: ' + listing.date + '\n')
            file.write('Job Location: ' + listing.location + '\n')
            file.write('Company: ' + listing.company + '\n')
            file.write('Listing URL: ' + listing.url + '\n')
            file.write('Job ID: ' + str(listing.job_id) + '\n')
            file.write('Description: ' + job.get_plaintext() + '\n')

    @staticmethod
    def write_formatted_text(file, text, max_words_per_line=25):
        for i, word in enumerate(text):
            file.write(word + ' ')
            if i % max_words_per_line == 0:
                file.write('\n')

    @staticmethod
    def retrieve_text(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        return text

    def clear_directory(self, directory):
        files = self.get_items_from_path(directory, item_type=Path.ALL)
        for file in files:
            os.unlink(file)

    @staticmethod
    def clear_files(directory):
        if os.path.exists(directory):
            for the_file in os.listdir(directory):
                file_path = os.path.join(directory, the_file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

    @staticmethod
    def create_directory(directory):
        if not os.path.exists(directory):
                os.makedirs(directory)

    def get_files_from_path(self, path):
        return self.get_items_from_path(path, item_type=Path.FILE)

    def get_folders_from_path(self, path):
        return self.get_items_from_path(path, item_type=Path.FOLDER)

    def get_items_from_path(self, path, item_type=Path.ALL):
        items = []
        contents = self.get_contents_of_path(path)
        for path in contents:
            if self.check_file_type(path, path_type=item_type):
                items.append(path)
        return items

    @staticmethod
    def get_contents_of_path(path):
        contents = []
        try:
            for file in os.listdir(path):
                absolute_path = os.path.join(path, file)
                contents.append(absolute_path)
        except Exception as e:
            logging.error(e)
        return contents

    @staticmethod
    def check_file_type(path, path_type=Path.FILE):
        match = False
        if path_type == Path.FILE:
            match = os.path.isfile(path)
        elif path_type == Path.FOLDER:
            match = os.path.isdir(path)
        elif path_type == Path.ALL:
            match = True
        else:
            logging.error('Invalid path type: ' + str(path_type))
        return match

    @staticmethod
    def get_json_data(json_path):
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def store_json_data(json_path, data):
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file)

    @staticmethod
    @storage_error()
    def get_config_file_text(file_name):
        file_path = LocalStorage.get_config_file_path(file_name)
        text = LocalStorage.retrieve_text(file_path)
        return text

    @staticmethod
    @storage_error()
    def get_config_file_path(file_name):
        file_path = os.path.join('Storage', 'config', file_name)
        if not os.path.isfile(file_path):
            raise ('File path does not exist: ' + file_path)
        return file_path

    @staticmethod
    def store_json_config(file_name, data):
        file_path = os.path.join(os.getcwd(), 'Storage', 'config', file_name)
        LocalStorage.store_json_data(file_path, data)

    @staticmethod
    def read_json_config(file_name):
        file_path = LocalStorage.get_config_file_path(file_name)
        data = LocalStorage.get_json_data(file_path)
        return data

    def clear_cache(self):
        self.clear_files(self.jobs_dir)
        self.clear_files(self.listings_dir)

    @storage_error()
    def clear_database(self):
        if not os.path.isfile(self.database_path):
            raise ('Database path does not point to file: ' + self.database_path)
        os.unlink(self.database_path)

    def store_jobs_in_database(self, jobs):
        self.database.add_jobs(jobs)

    @staticmethod
    def get_keyword_names():
        keywords_text = LocalStorage.get_config_file_text('keywords/keyword_list.txt')
        keyword_names = keywords_text.split('\n')
        keyword_names = [k.lower() for k in keyword_names]
        return keyword_names

    def get_free_job_id(self):
        return self.database.get_last_id() + 1

    def update_job_in_database(self, job):
        self.database.update_entry(job)

    @staticmethod
    def get_key():
        key_path = LocalStorage.get_config_file_path('key')
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        return key

    def close_database(self):
        self.database.close()

    def create_backup(self):
        file_name = TextFormatter.get_backup_name()
        zip_path = os.path.join(self.backup_dir, file_name)
        zip_file = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        for folder, subfolders, files in os.walk(self.config_dir):
            for file in files:
                if not self.is_src_file(file):
                    path = os.path.join(folder, file)
                    logging.info('Compressing file: {} -> {}'.format(path, zip_path))
                    zip_file.write(path)
        zip_file.close()

    @staticmethod
    def is_src_file(file):
        return file.endswith('.py') or file.endswith('.pyc') or file.endswith('.log')