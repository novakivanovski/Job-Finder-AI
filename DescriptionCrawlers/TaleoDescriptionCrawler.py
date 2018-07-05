from . import BaseDescriptionCrawler


class TaleoDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)

    def get_description(self):
        job_text = self.job.get_description()
        search_string = "'descRequisition', "
        start = job_text.find(search_string)
        if start != -1:  # taleo api
            start = start + len(search_string)
            end = job_text.find(']', start) + 1
            raw = job_text[start:end]
        else:
            raw = self.generic_search()
        return raw
