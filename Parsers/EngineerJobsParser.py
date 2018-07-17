import logging
from Job import JobMetadata
from Parsers.BaseParser import BaseParser


class EngineerJobsParser(BaseParser):
    def __init__(self):
        super().__init__('https://www.engineerjobs.com')

    def get_page_metadata_from_soup(self, page_soup):
        metadata = []
        for job_entry in page_soup.find_all(class_="jobrow"):
            job_data = []
            link = self.base_url + job_entry.find(class_="jobtitle")['data-mdref']
            items = job_entry.find_all('td')
            for item in items:
                job_data.append(item.text)
                logging.debug(item.text)
            m = JobMetadata(url=link, title=job_data[0], location=job_data[1],
                            company=job_data[2], date=job_data[3])
            metadata.append(m)
        return metadata
