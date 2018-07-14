from .BaseDescriptionCrawler import BaseDescriptionCrawler
import NetworkUtilities


class AkamaiDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)

    def get_description(self):
        raw = ''
        link = self.job.get_entry_url()
        for i in range(4):
            response = NetworkUtilities.get_html(link, allow_redirects=False)
            link = response.headers['Location']
        response = NetworkUtilities.get_html(link)
        self.job.set_description(response.text)
        self.job.set_url(link)
        soup = self.job.get_soup()
        tags = soup.find_all('p', style="margin-top:0px;margin-bottom:0px")
        for tag in tags:
            raw += tag.text + '\n'
        return raw