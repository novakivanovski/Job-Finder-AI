from Listers.BaseLister import BaseLister
from DataStructures.Listing import Listing
import re


class IndeedLister(BaseLister):
    def __init__(self, job_id, base_url='https://www.indeed.ca'):
        super().__init__(job_id, base_url=base_url)
        self.jobmap_regex = 'jobmap\[\d+\]'

    def get_listings_from_page(self, page):
        page_listings = []
        page_soup = page.get_soup()
        for job_entry in page_soup.find_all('h2', class_='jobtitle'):
            job_data = job_entry.find(class_='turnstileLink')
            posting_url = self.base_url + job_data.get('href')
            job_title = job_data.get('title')
            jobmap_item = re.findall(self.jobmap_regex, str(job_entry))[0]
            jobmap_data_regex = re.escape(jobmap_item) + '= (.+);'
            jobmap_data = re.search(jobmap_data_regex, page.text).group(1)
            location = re.search("loc:(.+)',country", jobmap_data).group(1).replace("'", '')
            company = re.search("cmp:(.+)',cmpesc", jobmap_data).group(1).replace("'", '')
            listing = Listing(url=posting_url, title=job_title, company=company,
                              location=location, job_id=self.get_job_id())
            page_listings.append(listing)
        return page_listings
