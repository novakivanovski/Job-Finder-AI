from DataStructures.Resume import Resume
from Tests import TestingTools


def test_header(resume):
    header = resume.header
    email = header.email
    phone_number = header.phone_number
    name = header.name
    website = header.website
    TestingTools.assert_equal(name, 'Novak Ivanovski')
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


def run():
    resume = Resume()
    test_header(resume)
    test_education(resume)

