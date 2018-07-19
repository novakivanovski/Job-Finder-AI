from Job import JobMetadata
from Listings.BaseListings import BaseListings


class EngineerJobsListings(BaseListings):
    def __init__(self, listings_text):
        super().__init__(listings_text, base_url='https://www.engineerjobs.com')

    def get_page_metadata(self, page_text):
        metadata = []
        page_soup = self.get_soup(page_text)
        for job_entry in page_soup.find_all(class_="jobrow"):
            job_data = []
            link = self.base_url + job_entry.find(class_="jobtitle")['data-mdref']
            items = job_entry.find_all('td')
            for item in items:
                job_data.append(item.text)
            m = JobMetadata(url=link, title=job_data[0], location=job_data[1],
                            company=job_data[2], date=job_data[3])
            metadata.append(m)
        return metadata
