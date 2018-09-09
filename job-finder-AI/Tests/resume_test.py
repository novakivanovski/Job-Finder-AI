from DataStructures.Resume import Resume
from Tests import TestingTools
from Utilities.ResumeParser import ResumeParser


def test_header(resume):
    header = resume.header
    email = header.email
    phone_number = header.phone_number
    name = header.name
    full_name = header.full_name
    website = header.website
    TestingTools.assert_equal(name, "Header")
    TestingTools.assert_equal(full_name, 'Novak Ivanovski')
    TestingTools.assert_equal(email, 'novakivanovski@gmail.com')
    TestingTools.assert_equal(phone_number, '289-442-5241')
    TestingTools.assert_equal(website, 'https://github.com/novakivanovski')


def test_education(resume):
    education = resume.education
    alma_mater = education.alma_mater
    degree = education.degree
    graduation_year = education.graduation_year
    awards = education.awards
    TestingTools.assert_equal(alma_mater, 'McMaster University')
    TestingTools.assert_equal(degree, 'Bachelor of Engineering')
    TestingTools.assert_equal(graduation_year, '2016')
    TestingTools.assert_equal(awards, "Awarded Dean’s Honour list for high level of academic achievement")


def test_highlights(resume):
    highlights = resume.highlights
    name = highlights.name
    TestingTools.assert_equal(name, "Highlights")
    TestingTools.assert_equal(highlights.items, ['Over 1 year of professional software engineering experience',
                                           'Excellent verbal and written communication skills, problem solving ability',
                                           'Self-starter who is able to learn quickly and take initiative to solve problems',
                                           'Well rounded individual adept at many programming languages and technologies'])


def test_projects(resume):
    projects = resume.projects
    name = projects.name
    TestingTools.assert_equal(name, "Projects")
    TestingTools.assert_equal(projects.items, ['Over 1 year of embedded software verification engineering experience for air systems and engine control units in the aerospace sector conforming to DO-178C standard',
                                               'Software development in C++ for eye tracking robot design project. Developed code for wireless communication, motion sensing, motor control feedback loop, and user input',
                                               'Contributions to open source software development in Java and Python'])


def test_experience(resume):
    experience = resume.experience
    name = experience.name
    job_titles = experience.job_titles
    job_dates = experience.job_dates
    job_locations = experience.job_locations
    TestingTools.assert_equal(name, "Experience")
    TestingTools.assert_equal(job_titles, ["Software Verification Engineer", "Junior Engineer"])
    TestingTools.assert_equal(job_dates, ["February 2018 – Present", "July 2016 – May 2017"])
    TestingTools.assert_equal(job_locations, ["Mississauga, Ontario"] * 2)


def run():
    resume_parser = ResumeParser()
    resume = Resume()
    test_header(resume)
    test_education(resume)
    test_highlights(resume)
    test_projects(resume)
    test_experience(resume)
