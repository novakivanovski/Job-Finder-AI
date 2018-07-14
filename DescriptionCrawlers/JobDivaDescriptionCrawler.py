from .BaseDescriptionCrawler import BaseDescriptionCrawler

class JobDivaDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)
    
    def get_description(self):
        soup = self.job.get_soup()
        raw = soup.find(class_='job_des').get_text()
        return raw