from . import BaseDescriptionCrawler


class SmoothHiringDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)
        
    def get_description(self):
        soup = self.job.get_soup()
        script_tags = soup.find_all('script')
        start = script_tags[10].text.find('{"id"')
        end = script_tags[10].text.find('};')
        raw = script_tags[10].text[start:end+1]
        return raw

