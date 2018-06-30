import requests
from bs4 import BeautifulSoup
import logging


def get_html_from_url(url):
    html_text = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    try:
        response = requests.get(url, headers=headers)
        html_text = response.text
    except IOError as e:
        logging.error('Request for ' + url + ' failed with exception: ' + str(e))
    return html_text


def get_soup_from_url(url):
    html_text = get_html_from_url(url)
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup

