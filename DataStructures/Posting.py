from bs4 import BeautifulSoup


class Posting:   # Acquired from PostingCrawler
    def __init__(self, listing_reference, page=None):
        self.page = page
        self.listing_reference = listing_reference
        self.description = ''

    def get_soup(self):
        soup = BeautifulSoup(self.page.text, 'html.parser')
        return soup

    def set_description(self, text):
        self.description = text

    def update_page(self, page):
        self.page = page

    def get_url(self):
        return self.page.url

    def get_text(self):
        return self.page.text
