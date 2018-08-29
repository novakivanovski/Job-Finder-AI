from Storage.LocalStorage import LocalStorage
import re


class Resume:
    def __init__(self):
        self.resume_config = self.load_resume_config()
        self.header = Header(self.resume_config['Header'])
        self.education = EducationSection(self.resume_config['Education'])
        self.highlights = HighlightSection(self.resume_config['Highlights of Qualification'])
        self.projects = RelevantProjectsSection(self.resume_config['Relevant Projects'])
        self.experience = ExperienceSection(self.resume_config['Experience'])

    @staticmethod
    def load_resume_config():
        return LocalStorage.read_json_config('resume_config.json')


class Item:
    def __init__(self, text, font_size=12):
        self.text = text
        self.font_size = font_size

    def get_text(self):
        return self.text


class Qualification:
    def __init__(self, items):
        self.items = items


class EducationQualification(Qualification):
    def __init__(self, items):
        super().__init__(items)
        self.school = items['School']
        self.year = items['Year']
        self.achievements = items['Achievements']
        self.degree = items['Degree']


class ExperienceQualification(Qualification):
    def __init__(self, items):
        super().__init__(items)
        self.job_title = items['Job Title']
        self.date = items['Employment Date']
        self.responsibilities = items['Job Responsibilities']
        self.achievements = items['Achievements']


class HighlightQualification(Qualification):
    def __init__(self, items):
        super().__init__(items)


class Header:
    def __init__(self, header_data):
        self.name = header_data['Name']
        self.email = header_data['Email']
        self.website = header_data['Website']
        self.phone_number = header_data['Phone']


class Section:
    def __init__(self, text, name=''):
        self.name = name
        self.text = text


class EducationSection(Section):
    def __init__(self, text):
        super().__init__(text, name='Education')
        self.alma_mater = self.get_alma_mater()
        self.degree = self.get_degree()
        self.graduation_year = self.get_graduation_year()
        self.awards = self.get_awards()

    def get_alma_mater(self):
        university_regex = '[A-Z|a-z]+ University'
        alma_mater = re.findall(university_regex, self.text)
        return alma_mater[0]

    def get_degree(self):
        degree_regex = 'Bachelor of [A-Z][a-z]+'
        degree = re.findall(degree_regex, self.text)
        return degree[0]

    def get_graduation_year(self):
        year_regex = 'Class of [0-9]{4}'
        graduation_match = re.findall(year_regex, self.text)[0]
        graduation_year = graduation_match[-4:]
        return graduation_year

    def get_awards(self):
        awards_regex = 'Awarded .+$'
        awards = re.findall(awards_regex, self.text)
        return awards[0]


class HighlightSection(Section):
    def __init__(self, text):
        super().__init__(text, name='Highlights of Qualification')


class ExperienceSection(Section):
    def __init__(self, text):
        super().__init__(text, name='Education')


class RelevantProjectsSection(Section):
    def __init__(self, text):
        super().__init__(text, name='Relevant Projects')




