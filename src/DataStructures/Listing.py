class Listing:   # Acquired from Crawler - general info
    def __init__(self, title='', date='', location='', company='', url='', job_id=0):
        self.title = title
        self.date = date
        self.location = location
        self.company = company
        self.url = url
        self.job_id = job_id

    def set_id(self, job_id):
        self.job_id = job_id

    def get_url(self):
        return self.url

    def get_id(self):
        return self.job_id
