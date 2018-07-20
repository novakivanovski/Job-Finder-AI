from .BasePostingCrawler import BasePostingCrawler
import json


class BrassRingPostingCrawler(BasePostingCrawler):
    def __init__(self, posting):
        super().__init__(posting)

    def get_description(self):
        soup = self.posting.get_soup()
        text = str(soup.find('input', id='preLoadJSON'))
        start = text.find('{"SmartSearchJSONValue"')
        end = text.find("'/>")
        json_data = json.loads(text[start:end])
        raw = ''
        for item in json_data['postingdetails']['postingDetailQuestions']:
            raw = raw + item['AnswerValue'] + '\n'
        return raw
