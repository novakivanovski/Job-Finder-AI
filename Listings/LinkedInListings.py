from Listings.BaseListings import BaseListings


class IndeedListings(BaseListings):
    def __init__(self):
        super().__init__('https://www.linkedin.com')

    def get_page_metadata(self, listing):
        pass
