import requests
from bs4 import BeautifulSoup
import logging


def get_html_from_url(url, *args, **kwargs):
    html_text = ''
    try:
        response = requests.get(url, *args, **kwargs)
        html_text = response.text
    except Exception as e:
        logging.error('Request for ' + url + ' failed with exception: ' + str(e))
    return html_text


def get_soup_from_url(url):
    html_text = get_html_from_url(url)
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup

