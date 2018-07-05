from bs4 import BeautifulSoup


class Job:
    def __init__(self, job_metadata, job_description):
        self.metadata = job_metadata
        self.description = job_description

    def get_id(self):
        return self.metadata.job_id

    def get_soup(self):
        return self.description.soup

    def get_description(self):
        return self.description.text

    def set_description(self, text):
        self.description.text = text
        self.description.soup = BeautifulSoup(text)

    def set_url(self, url):
        self.description.url = url

    def get_entry_url(self):
        return self.metadata.origin_url


class JobMetadata:   # Acquired from Crawler - general info
    def __init__(self, title='', date='', location='', company='', url='', job_id=0):
        self.title = title
        self.date = date
        self.location = location
        self.company = company
        self.origin_url = url
        self.job_id = job_id


# Acquired from JobParser - job description document

class JobDescription:
    def __init__(self, soup):
        self.url = None
        self.keywords = None
        self.passed = False
        self.soup = soup
        self.text = soup.text
        self.raw = ''

