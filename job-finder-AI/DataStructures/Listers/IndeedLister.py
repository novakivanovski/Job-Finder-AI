from DataStructures.Listers.BaseLister import BaseLister


class IndeedLister(BaseLister):
    def __init__(self):
        super().__init__('https://www.indeed.ca')

    def get_listings_from_page(self, listing):
        pass
