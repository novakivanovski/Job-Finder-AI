from .BasePostingCrawler import BasePostingCrawler
import requests
from bs4 import BeautifulSoup
import json
from Utilities.ParseUtility import ParseUtility


class GooglePostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        url = self.posting.get_url()
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
        r_j = ParseUtility.get_value_between_strings(r.text, "'r-j','", "',")
        link = 'https://careers.google.com/postings/|'
        payload = '7|3|7|' + link + r_j + '|22|' + xsrf_token + '|_|getpostingById|4o|1|2|3|4|5|6|1|7|7|Ce9YM_|'
        headers = self.headers
        headers['content-type'] = 'text/x-gwt-rpc; charset=UTF-8'
        headers['origin'] = 'https://careers.google.com'
        headers['x-gwt-permutation'] = js_cache[6:-9]
        r = s.post('https://careers.google.com/postings/r-j', headers=headers, data=payload)
        raw = r.text
        return raw
