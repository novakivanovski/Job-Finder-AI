import requests
import logging
from Job import Job

class JobManager:
    def __init__(self):
        self.jobs = []
        self.headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}

    def add_job(self, job_metadata):
        j = Job(job_metadata)
        self.store_job(j)

    def store_job(self, job):
        self.jobs.append(job)

    def clear_jobs(self):
        self.jobs = []

    def update_title(self, job, title):
        job.title = title

    def update_location(self, job, location):
        job.location = location

    def resync_html(self, job):
        html_source = get_job_html(job.url)
        job.html = html_source

    def update_metadata(self, metadata, job):
        job.metadata = metadata



'''
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
     
'''
