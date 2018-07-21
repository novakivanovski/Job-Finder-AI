from bs4 import BeautifulSoup


class Posting:   # Acquired from PostingCrawler
    def __init__(self, listing_reference, page=None):
        self.page = page
        self.listing_reference = listing_reference
        self.plaintext = ''

    def get_soup(self):
        soup = BeautifulSoup(self.page.text, 'html.parser')
        return soup

    def get_plaintext(self):
        return self.plaintext

    def set_plaintext(self, text):
        self.plaintext = text

    def set_page(self, page):
        self.page = page

    def get_url(self):
        return self.page.url

    def get_text(self):
        return self.page.text

