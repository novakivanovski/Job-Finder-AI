from Storage.LocalStorage import LocalStorage
import docx2txt
import re


class ResumeParser:
    def __init__(self):
        self.header = ''
        self.resume_path = LocalStorage.get_config_file_path('resume/Resume.docx')
        self.text = self.extract_text(self.resume_path)
        self.section_whitelist = self.load_section_whitelist()
        self.section_names = self.get_section_names(self.section_whitelist)
        self.sections = self.get_sections()
        self.resume_config = self.get_resume_config()
        self.store_resume_config()

    def get_sections(self):
        sections = {}
        for section_name in self.section_names:
            section_text = self.get_section_text(section_name)
            sections[section_name] = section_text
        return sections

    @staticmethod
    def extract_text(docx_path):
        pattern = '\n+'
        raw_text = docx2txt.process(docx_path)
        text = re.sub(pattern, '\n', raw_text)
        return text

    @staticmethod
    def load_section_whitelist():
        section_names = LocalStorage.get_config_file_text('resume/resume_sections.txt')
        return section_names.split('\n')

    def get_section_names(self, section_whitelist):
        resume_lines = self.text.split('\n')
        section_names = []
        for line in resume_lines:
            if line in section_whitelist:
                section_names.append(line)
        return section_names

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

    def get_resume_config(self):
        resume_config = dict(
            Header=self.get_header(),
            Education=self.get_education(),
            Highlights=self.get_highlights(),
            Experience=self.get_experience(),
            Projects=self.get_projects()
                             )
        return resume_config

    def store_resume_config(self):
        LocalStorage.store_json_config('resume/resume_config.json', self.resume_config)

    def get_header(self):
        end = self.get_first_section_index()
        self.header = self.text[:end]
        header_data = dict(Email=self.get_email(),
                           Phone=self.get_phone(),
                           Name=self.get_name(),
                           Website=self.get_website())
        return header_data

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

    def get_education(self):
        education_data = dict(Alma_Mater=self.get_alma_mater(),
                              Degree=self.get_degree(),
                              Year=self.get_graduation_year(),
                              Awards=self.get_awards())
        return education_data

    def get_alma_mater(self):
        university_regex = '[A-Z|a-z]+ University'
        alma_mater = re.findall(university_regex, self.sections['Education'])
        return alma_mater[0]

    def get_degree(self):
        degree_regex = 'Bachelor of [A-Z][a-z]+'
        degree = re.findall(degree_regex, self.sections['Education'])
        return degree[0]

    def get_graduation_year(self):
        year_regex = 'Class of [0-9]{4}'
        graduation_matches = re.findall(year_regex, self.sections['Education'])
        graduation_match = graduation_matches[0]
        graduation_year = graduation_match[-4:]
        return graduation_year

    def get_awards(self):
        awards_regex = 'Awarded .+$'
        awards = re.findall(awards_regex, self.sections['Education'])
        return awards[0]

    @staticmethod
    def read_resume_config():
        resume_config = LocalStorage.read_json_config('resume/resume_config.json')
        return resume_config

    def get_highlights(self):
        highlights = self.sections['Highlights of Qualification']
        return self.convert_to_list(highlights)

    def get_experience(self):
        text = self.sections['Experience']
        lines = text.split('\n')
        job_titles = self.get_job_titles(lines)
        job_locations = self.get_job_locations(text)
        job_dates = self.get_job_dates(text)
        job_tasks = self.get_job_tasks(lines, job_locations, job_titles)
        experience_data = dict(Titles=job_titles,
                               Locations=job_locations,
                               Dates=job_dates,
                               Tasks=job_tasks)
        return experience_data

    @staticmethod
    def get_job_titles(lines):
        job_titles = [line for line in lines if 'Engineer' in line]
        return job_titles

    @staticmethod
    def get_job_locations(text):
        locations_regex = '\S+, Ontario'
        locations_matches = re.findall(locations_regex, text)
        return locations_matches

    @staticmethod
    def get_job_dates(text):
        date_regex = '\S+ \d{4} – (?:\S+ \d{4}|Present)'
        date_matches = re.findall(date_regex, text)
        return date_matches

    def get_job_tasks(self, lines, job_locations, job_titles):
        current_job = 0
        job_tasks = []
        for location in job_locations:
            job_tasks.append([])

        for line in lines:
            if job_titles[current_job] in line or job_locations[current_job] in line or not line:
                pass
            elif self.next_job_in_line(job_titles, current_job, line):
                current_job += 1
            else:
                job_tasks[current_job].append(line)
        return job_tasks

    @staticmethod
    def next_job_in_line(job_titles, current_job, line):
        next_job = current_job + 1
        num_jobs = len(job_titles)
        if next_job >= num_jobs:
            return False
        next_job_name = job_titles[next_job]
        return next_job_name in line

    def get_projects(self):
        projects = self.sections['Relevant Projects']
        return self.convert_to_list(projects)

    @staticmethod
    def convert_to_list(newline_string):
        newline_split_list = newline_string.split('\n')
        nonempty_list = [item for item in newline_split_list if item]
        return nonempty_list


