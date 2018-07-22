from bs4 import BeautifulSoup


class Posting:   # Acquired from Crawler
    def __init__(self, listing_reference, page):
        self.page = page
        self.listing_reference = listing_reference

    def get_soup(self):
        soup = BeautifulSoup(self.page.text, 'html.parser')
        return soup

    def set_page(self, page):
        self.page = page

    def get_url(self):
        return self.page.url

    def get_text(self):
        return self.page.text

    def get_id(self):
        return self.listing_reference.get_id()

