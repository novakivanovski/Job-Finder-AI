class Item:
    def __init__(self, text, font_size=12):
        self.text = text
        self.font_size = font_size

    def get_text(self):
        return self.text


class BulletItem(Item):
    def __init__(self, text):
        super().__init__(text)

    def get_text(self):
        return '• ' + self.text


class BigItem(Item):
    def __init__(self, text):
        super().__init__(text, font_size=18)


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
        self.highlights = items['Highlights']


class Header:
    def __init__(self, items, highlights):
        self.name = items['Name']
        self.email = items['Email']
        self.website = items['Website']
        self.phone_number = items['Phone Number']
        self.highlights = highlights


class Section:
    def __init__(self, qualifications, name=''):
        self.name = name
        self.qualifications = qualifications

    def get_encoded(self):  # Need implementation to format section and encode to docx.
        pass


class EducationSection:
    def __init__(self, qualifications):
        super().__init__(qualifications, name='Education')

