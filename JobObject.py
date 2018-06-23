import requests


class JobObject:
 
    def __init__(self, title='No Title', url='', location='', company='', date=''):
        self.headers = {}
        self.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        self.keywords = []
        self.text = ''
        base_url = 'https://www.engineerjobs.com'
        self.url = ''
        if url:
            try:
                r = requests.get(base_url + url, headers=self.headers)
                self.url = r.url
                self.text = r.text
            except Exception as e:
                self.url = base_url + url
                self.text = ''
                    
        self.title = title
        self.location = location
        self.company = company
        self.date = date
        self.raw =  ''
        self.passed = False
     
