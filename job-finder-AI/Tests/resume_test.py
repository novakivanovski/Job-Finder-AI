from DataStructures.Resume import ResumeConfig
from Utilities.ResumeParser import ResumeParser
from Tests import TestingTools


def test_constructor():
    my_resume = ResumeConfig()
    test_highlights = ["Over 1 year of professional software engineering experience", "Excellent verbal and written communication skills, problem solving ability"]
    test_projects = ["Contributions to open source software development in Java and Python", "Software development in C++ for eye tracking robot design project"]
    test_experience = ["Software Verification Engineer", "Junior Engineer"]
    TestingTools.assert_equal(my_resume.title, 'Novak Ivanovski')
    TestingTools.assert_equal(my_resume.email, 'novakivanovski@gmail.com')
    TestingTools.assert_equal(my_resume.phone_number, '289-442-5241')
    TestingTools.assert_equal(my_resume.website, 'https://github.com/novakivanovski')
    TestingTools.assert_equal(my_resume.highlights, test_highlights)
    TestingTools.assert_equal(my_resume.education, 'Bachelor of Engineering, Engineering Physics'),
    TestingTools.assert_equal(my_resume.projects, test_projects)
    TestingTools.assert_equal(my_resume.experience, test_experience)


def run():
    r = ResumeParser()
    education = r.get_section_data('Education')
    print(education)
    experience = r.get_section_data('Experience')
    print(experience)

