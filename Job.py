from bs4 import BeautifulSoup


class Job:
    def __init__(self, job_metadata):
        self.metadata = job_metadata
        self.description = JobDescription()

    def get_id(self):
        return self.metadata.job_id

    def set_id(self, job_id):
        self.metadata.job_id = job_id

    def get_soup(self):
        if self.description.soup:
            soup = self.description.soup
        else:
            soup = BeautifulSoup(self.description.text, 'html.parser')
        return soup

    def get_description(self):
        return self.description.text

    def set_description(self, text):
        self.description.text = text

    def update_soup(self):
        if self.description.text:
            self.description.soup = BeautifulSoup(self.description.text, 'html.parser')

    def set_url(self, url):
        self.description.url = url

    def get_entry_url(self):
        return self.metadata.entry_url

    def get_url(self):
        return self.description.url

    def get_raw(self):
        return self.description.raw

    def get_title(self):
        return self.metadata.title

    def get_keywords(self):
        return self.description.keywords

    def set_keywords(self, keywords):
        self.description.keywords = keywords

    def set_raw(self, text):
        self.description.raw = text

    def has_description(self):
        has_description = self.description.text is not '' and self.description.text is not None
        return has_description


class JobMetadata:   # Acquired from Crawler - general info
    def __init__(self, title='', date='', location='', company='', url='', job_id=0):
        self.title = title
        self.date = date
        self.location = location
        self.company = company
        self.entry_url = url
        self.job_id = job_id

    def set_id(self, job_id):
        self.job_id = job_id


# Acquired from JobParser - job description document

class JobDescription:
    def __init__(self):
        self.url = None
        self.keywords = None
        self.passed = False
        self.soup = ''
        self.text = ''
        self.raw = ''

