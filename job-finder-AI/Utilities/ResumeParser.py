from Storage.LocalStorage import LocalStorage
import docx2txt
import re


class ResumeParser:
    def __init__(self):
        self.resume_path = LocalStorage.get_config('Resume.docx')
        self.text = self.extract_text(self.resume_path)
        self.section_whitelist = self.load_section_whitelist()
        self.resume_sections = self.get_section_names()

    @staticmethod
    def extract_text(docx_path):
        pattern = '\n+'
        raw_text = docx2txt.process(docx_path)
        text = re.sub(pattern, '\n', raw_text)
        return text

    @staticmethod
    def load_section_whitelist():
        section_names_path = LocalStorage.get_config('resume_sections.txt')
        section_names = LocalStorage.retrieve_text(section_names_path)
        return section_names.split('\n')

    def get_section_names(self):
        resume_lines = self.text.split('\n')
        resume_sections = []
        for line in resume_lines:
            if line in self.section_whitelist:
                resume_sections.append(line)
        return resume_sections

    def get_section_data(self, section_name):
        start = self.text.find(section_name)
        section_index = self.resume_sections.index(section_name)
        if self.is_last_section(section_index):
            return self.text[start:]
        next_section = self.resume_sections[section_index + 1]
        end = self.text.find(next_section)
        return self.text[start:end]

    def is_last_section(self, section_index):
        return section_index == len(self.resume_sections) - 1






