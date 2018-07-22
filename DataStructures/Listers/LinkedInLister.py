from DataStructures.Listers.BaseLister import BaseLister


class IndeedLister(BaseLister):
    def __init__(self):
        super().__init__('https://www.linkedin.com')

    def get_listings_from_page(self, listing):
        pass
