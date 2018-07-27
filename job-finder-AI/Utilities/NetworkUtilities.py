import requests
from bs4 import BeautifulSoup
from DataStructures.Page import Page
from Utilities.ApplicationExceptions import NetworkError


def get_page(url, *args, **kwargs):
    response = get(url, *args, **kwargs)
    page = Page(response.text, response.url)
    return page


def get_html(url, *args, **kwargs):
    response = get(url, *args, **kwargs)
    html_text = response.text
    return html_text


def get_session():
    try:
        session = requests.session()
    except Exception:
        raise NetworkError('Error getting session.')
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
        raise NetworkError('Error getting response.')
    return response
