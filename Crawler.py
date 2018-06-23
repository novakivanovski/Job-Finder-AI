import requests
from math import ceil
from bs4 import BeautifulSoup
from JobObject import JobObject
from multiprocessing import Process, Manager, Pool as ThreadPool
from threading import Thread
from time import time, sleep
from FilterAlgorithm import FilterAlgorithm

class Crawler:
    
    def __init__(self, file_path, frequency='1'):
        self.jobs = []
        self.test_mode = False
        self.num_jobs = 0
        self.percents = [0, 0, 0]
        self.num_pages = 0
        self.threads = []
        self.base_url = "https://www.engineerjobs.com/jobs/software-engineering/canada/ontario/?f=" + frequency + "&page="
        self.jobs_per_page = 20
        self.details = []
        self.f = FilterAlgorithm(file_path)

    def dummy_call(self):    
        html_data = requests.get(self.base_url)
        jobs_string = BeautifulSoup(html_data.text, 'html.parser').find(id="search-results-count").get_text()
        number_of_jobs = self.get_number_of_jobs(jobs_string)
        num_pages = self.get_num_pages(number_of_jobs)
        # need to send twice because bug causes job count to be displayed incorrectly on first page sometimes
        html_data = requests.get(self.base_url + str (num_pages))
        jobs_string = BeautifulSoup(html_data.text, 'html.parser').find(id="search-results-count").get_text()
        number_of_jobs = self. get_number_of_jobs(jobs_string)
        self.num_jobs = number_of_jobs
        self.num_pages = self.get_num_pages(number_of_jobs)

    def get_number_of_jobs(self, jobs_string):
        jobs_regex  = "fill this in"
        return 0

    def get_num_pages(self, num_jobs):
        return ceil(num_jobs / 20)
    
    def get_job_details(self, page_number, q):
        url = self.base_url + str(page_number + 1)
        html_data = requests.get(url)
        soup = BeautifulSoup(html_data.text, 'html.parser')
        for row in soup.find_all(class_="jobrow"):
            job_data = []
            link = row.find(class_ = "jobtitle")['data-mdref']
            job_data.append(link)
            cells = row.find_all('td')
            for cell in cells:
                job_data.append(cell.text)
            q.put(job_data)
        
    def create_jobs(self, q, job):
        link = job[0]
        title = job[1]
        location = job[2]
        company = job[3]
        date = job[4]
        j = JobObject(title, link, location, company, date)
        q.put(j)

    def percent_complete(self, max_size, bar, q):
        q_size = 0
        while q_size < max_size:
            q_size = q.qsize()
            self.percents[bar] = (q_size / max_size) * 100
            sleep(1)

    def multi_thread(self):
        max_threads = 400
        q = Manager().Queue(maxsize=0)
        start = time()
        threads = []
        
        if self.test_mode:
            self.num_pages = 1
            self.num_jobs = 20

        loading = Thread(target=self.percent_complete, args=(self.num_jobs, 0, q))
        loading.start()

        for page_num in range(self.num_pages):
            t = Thread(target=self.get_job_details, args=(page_num, q))
            threads.append(t)
            t.start()
        
        for thrd in threads:
            thrd.join()

        loading.join()

        threads = []
        
        while not q.empty():
            self.details.append(q.get())

        for job in self.details:
            t = Thread(target=self.create_jobs, args =(q, job))
            threads.append(t)
            
        num_threads = len(threads)
        num_passes = int(ceil(num_threads/max_threads))
        loading = Thread(target=self.percent_complete, args=(num_threads, 1, q))
        loading.start()

        for k in range(num_passes):
            start = k * max_threads
            end = (k + 1) * max_threads
            for i in range(start, end):
                if i < num_threads:
                    threads[i].start()
            for i in range(start, end):
                if i < num_threads:
                    threads[i].join()

        loading.join()

        while not q.empty():
            self.jobs.append(q.get())
        
        loading = Thread(target=self.percent_complete, args=(num_threads, 2, q))
        loading.start()
        self.f.extract(self.jobs, q)
        self.num_jobs = len (self.jobs)
        loading.join()

     
    def crawl(self):
        self.jobs = []
        self.details = []
        self.dummy_call()
        self.multi_thread()