from Parsers.BaseParser import BaseParser


class IndeedParser(BaseParser):
    def __init__(self):
        super().__init__('https://www.indeed.ca')

    def get_page_metadata_from_soup(self, page_soup):  # need to fill this in
        metadata = []
        search_tag = 'jobKeysWithInfo'
        return search_tag, metadata
