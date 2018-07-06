import requests
from bs4 import BeautifulSoup
import logging


def get_html(url, *args, **kwargs):
    html_text = ''
    try:
        response = requests.get(url, *args, **kwargs)
        html_text = response.text
    except Exception as e:
        logging.error('Request for ' + url + ' failed with exception: ' + str(e))
    return html_text


def get_session():
    session = None
    try:
        session = requests.session()
    except Exception as e:
        logging.error('Unable to establish session: ' + str(e))
    return session


def get_soup(url):
    html_text = get_html(url)
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup

