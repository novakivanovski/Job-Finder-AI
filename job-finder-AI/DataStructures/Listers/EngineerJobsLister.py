from DataStructures.Listing import Listing
from DataStructures.Listers.BaseLister import BaseLister


class EngineerJobsLister(BaseLister):
    def __init__(self, job_id, base_url='https://www.engineerjobs.com'):
        super().__init__(job_id, base_url=base_url)

    def get_listings_from_page(self, page):
        page_listings = []
        page_soup = page.get_soup()
        for job_entry in page_soup.find_all(class_="jobrow"):
            job_data = []
            job_id = self.get_job_id()
            link = self.base_url + job_entry.find(class_="jobtitle")['data-mdref']
            items = job_entry.find_all('td')
            for item in items:
                job_data.append(item.text)
            listing = Listing(url=link, title=job_data[0], location=job_data[1],
                              company=job_data[2], date=job_data[3], job_id=job_id)
            page_listings.append(listing)
        return page_listings
