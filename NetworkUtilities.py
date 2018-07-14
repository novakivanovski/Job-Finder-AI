import requests
from bs4 import BeautifulSoup
import logging


def get_html(url, *args, **kwargs):
    html_text = ''
    response = get(url, *args, **kwargs)
    if response:
        html_text = response.text
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


def get(url, *args, **kwargs):
    kwargs['timeout'] = 5
    try:
        response = requests.get(url, *args, **kwargs)
    except Exception:
        raise
    return response
