from bs4 import BeautifulSoup


class Page:
    def __init__(self, text, url):
        self.text = text
        self.url = url

    def get_soup(self):
        soup = BeautifulSoup(self.text, 'html.parser')
        return soup
