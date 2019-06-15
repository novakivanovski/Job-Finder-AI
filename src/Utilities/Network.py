import requests
from bs4 import BeautifulSoup
from DataStructures.Page import Page
from Utilities.ApplicationExceptions import network_error


def get_page(url, *args, **kwargs):
    response = get(url, *args, **kwargs)
    page = Page(response.text, response.url)
    return page


def get_html(url, *args, **kwargs):
    response = get(url, *args, **kwargs)
    html_text = response.text
    return html_text


@network_error()
def get_session():
    session = requests.session()
    return session


def get_soup(url):
    html_text = get_html(url)
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup


@network_error()
def get(url, *args, **kwargs):
    kwargs['timeout'] = 5
    response = requests.get(url, *args, **kwargs)
    return response
