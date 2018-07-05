from abc import ABCMeta, abstractmethod


class BaseDescriptionCrawler(metaclass=ABCMeta):
    def __init__(self, job):
        self.job = job
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        self.tags = ['li', 'p', 'article', 'pre']

    def generic_search(self):
        raw = ''
        soup = self.job.get_soup()
        for tag in self.tags:
            instances = soup.find_all(tag)
            for instance in instances:
                raw += ' ' + instance.get_text()
        return raw

    @abstractmethod
    def get_description(self):
        pass
