from DataStructures.Listing import Listing
from DataStructures.Listers.BaseLister import BaseLister


class EngineerJobsLister(BaseLister):
    def __init__(self, base_url):
        super().__init__(base_url)

    def get_listing_from_page(self, page):
        page_listings = []
        page_soup = page.get_soup()
        for job_entry in page_soup.find_all(class_="jobrow"):
            job_data = []
            link = self.base_url + job_entry.find(class_="jobtitle")['data-mdref']
            items = job_entry.find_all('td')
            for item in items:
                job_data.append(item.text)
            listing = Listing(url=link, title=job_data[0], location=job_data[1],
                              company=job_data[2], date=job_data[3])
            page_listings.append(listing)
        return page_listings