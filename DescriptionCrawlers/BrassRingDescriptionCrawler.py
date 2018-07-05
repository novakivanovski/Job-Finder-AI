from . import BaseDescriptionCrawler
import json


class BrassRingDescriptionCrawler(BaseDescriptionCrawler):
    def __init__(self, job):
        super().__init__(job)

    def get_description(self):
        soup = self.job.get_soup()
        text = str(soup.find('input', id='preLoadJSON'))
        start = text.find('{"SmartSearchJSONValue"')
        end = text.find("'/>")
        json_data = json.loads(text[start:end])
        raw = ''
        for item in json_data['Jobdetails']['JobDetailQuestions']:
            raw = raw + item['AnswerValue'] + '\n'
        return raw
