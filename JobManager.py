from Job import Job, JobDescription
import NetworkUtilities


class JobManager:
    def __init__(self):
        self.jobs = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}
        self.num_jobs = 0
        self.job_id = 0

    def add_jobs_from_queue(self, queue):
        while not queue.empty():
            metadata = queue.get()
            metadata.job_id = self.job_id
            self.add_job(metadata)
            self.job_id += 1

    def add_job(self, job_metadata):
        j = Job(job_metadata)
        self.store_job(j)

    def store_job(self, job):
        self.jobs.append(job)

    def get_num_jobs(self):
        return self.num_jobs

    @staticmethod
    def update_job_description(job):
        description_text = NetworkUtilities.get_html_from_url(job.entry_url)
        description = JobDescription(description_text)
        job.description = description

    def clear_jobs(self):
        self.jobs = []

    def update_title(self, job, title):
        job.title = title

    def update_location(self, job, location):
        job.location = location

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
