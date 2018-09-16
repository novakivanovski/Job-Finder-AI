from Storage.LocalStorage import LocalStorage


class Resume:
    def __init__(self):
        self.resume_config = self.load_resume_config()
        self.header = HeaderSection(self.resume_config['Header'])
        self.education = EducationSection(self.resume_config['Education'])
        self.highlights = HighlightSection(self.resume_config['Highlights'])
        self.projects = ProjectsSection(self.resume_config['Projects'])
        self.experience = ExperienceSection(self.resume_config['Experience'])

    @staticmethod
    def load_resume_config():
        return LocalStorage.read_json_config('resume_config.json')


class HeaderSection:
    def __init__(self, header_data):
        self.name = "Header"
        self.full_name = header_data['Name']
        self.email = header_data['Email']
        self.website = header_data['Website']
        self.phone_number = header_data['Phone']


class EducationSection:
    def __init__(self, education_data):
        self.name = "Education"
        self.alma_mater = education_data['Alma_Mater']
        self.degree = education_data['Degree']
        self.graduation_year = education_data['Year']
        self.awards = education_data['Awards']


class ExperienceSection:
    def __init__(self, experience_data):
        self.name = "Experience"
        self.job_titles = experience_data['Titles']
        self.job_locations = experience_data['Locations']
        self.job_dates = experience_data['Dates']
        self.job_tasks = experience_data['Tasks']
        self.job_titles_to_dates = dict(zip(self.job_titles, self.job_dates))
        self.job_titles_to_locations = dict(zip(self.job_titles, self.job_locations))
        self.job_titles_to_tasks = dict(zip(self.job_titles, self.job_tasks))


class GenericSection:
    def __init__(self, item_list, name=''):
        self.name = name
        self.items = item_list
        self.text = ' '.join(item_list)


class HighlightSection(GenericSection):
    def __init__(self, item_list):
        super().__init__(item_list, name="Highlights")


class ProjectsSection(GenericSection):
    def __init__(self, item_list):
        super().__init__(item_list, name="Projects")
