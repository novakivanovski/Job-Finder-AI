from Storage.LocalStorage import LocalStorage
import docx2txt
import re


class ResumeParser:
    def __init__(self):
        self.resume_path = LocalStorage.get_config_file_path('Resume.docx')
        self.text = self.extract_text(self.resume_path)
        self.section_whitelist = self.load_section_whitelist()
        self.section_names = self.get_section_names(self.section_whitelist)
        self.header = self.get_header()
        self.resume_config = self.get_resume_config(self.section_names)

    @staticmethod
    def extract_text(docx_path):
        pattern = '\n+'
        raw_text = docx2txt.process(docx_path)
        text = re.sub(pattern, '\n', raw_text)
        return text

    @staticmethod
    def load_section_whitelist():
        section_names = LocalStorage.get_config_file_text('resume_sections.txt')
        return section_names.split('\n')

    def get_section_names(self, section_whitelist):
        resume_lines = self.text.split('\n')
        resume_sections = []
        for line in resume_lines:
            if line in section_whitelist:
                resume_sections.append(line)
        return resume_sections

    def get_section_text(self, section_name):
        start = self.text.find(section_name) + len(section_name)
        section_index = self.section_names.index(section_name)
        if self.is_last_section(section_index):
            return self.text[start:]
        next_section = self.section_names[section_index + 1]
        end = self.text.find(next_section)
        return self.text[start:end]

    def is_last_section(self, section_index):
        return section_index == len(self.section_names) - 1

    def get_resume_config(self, section_names):
        resume_config = {}
        for section_name in section_names:
            section_text = self.get_section_text(section_name)
            resume_config[section_name] = section_text
        resume_config['Header'] = {}
        resume_config['Header']['Email'] = self.get_email()
        resume_config['Header']['Phone'] = self.get_phone()
        resume_config['Header']['Name'] = self.get_name()
        resume_config['Header']['Website'] = self.get_website()
        return resume_config

    def store_resume_config(self):
        LocalStorage.store_json_config('resume_config.json', self.resume_config)

    def get_resume_map(self):
        return self.resume_config

    def get_header(self):
        end = self.get_first_section_index()
        return self.text[:end]

    def get_first_section_index(self):
        first_section = self.section_names[0]
        first_section_index = self.text.find(first_section)
        return first_section_index

    def get_email(self):
        email_regex = '.+[@].+[.].+'
        email_matches = re.findall(email_regex, self.header)
        return email_matches[0]

    def get_phone(self):
        phone_regex = '\d{3}-\d{3}-\d{4}'
        phone_matches = re.findall(phone_regex, self.header)
        return phone_matches[0]

    def get_name(self):
        name_regex = '[A-Z][a-z]+ [A-Z][a-z]+'
        name_matches = re.findall(name_regex, self.header)
        return name_matches[0]

    def get_website(self):
        website_regex = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+' \
                     '[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.' \
                     '[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}' \
                     '|www\.[a-zA-Z0-9]\.[^\s]{2,})'
        website_matches = re.findall(website_regex, self.header)
        return website_matches[0]

    @staticmethod
    def read_resume_config():
        resume_config = LocalStorage.read_json_config('resume_config.json')
        return resume_config








