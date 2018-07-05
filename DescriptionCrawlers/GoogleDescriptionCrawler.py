from . import BaseDescriptionCrawler
import requests
from bs4 import BeautifulSoup
import json


class GoogleDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)

    def get_description(self):
        url = self.job.get_entry_url()
        attrs = {'type': 'text/javascript'}
        s = requests.Session()
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        tags = soup.find_all('script', attrs=attrs)
        text = tags[1].text
        start = text.find('{')
        end = text.find('}') + 1
        f_text = text[start:end].replace("'", '"')
        f_text = f_text.replace('\\', '\\\\')
        xsrf_token = json.loads(f_text)['xsrfToken']
        js_cache = tags[3]['src']
        cache_url = 'https://careers.google.com' + js_cache
        r = s.get(cache_url)
        r_j = self.get_field(r.text, "'r-j','", "',")
        link = 'https://careers.google.com/jobs/|'
        payload = '7|3|7|' + link + r_j + '|22|' + xsrf_token + '|_|getJobById|4o|1|2|3|4|5|6|1|7|7|Ce9YM_|'
        headers = self.headers
        headers['content-type'] = 'text/x-gwt-rpc; charset=UTF-8'
        headers['origin'] = 'https://careers.google.com'
        headers['x-gwt-permutation'] = js_cache[6:-9]
        r = s.post('https://careers.google.com/jobs/r-j', headers=headers, data=payload)
        raw = r.text
        return raw
