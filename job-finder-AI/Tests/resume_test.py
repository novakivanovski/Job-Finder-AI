from Utilities.ResumeParser import ResumeParser
from Tests import TestingTools


def test_resume():
    r = ResumeParser()
    email = r.get_email()
    phone = r.get_phone()
    name = r.get_name()
    website = r.get_website()
    TestingTools.assert_equal(name, 'Novak Ivanovski')
    TestingTools.assert_equal(email, 'novakivanovski@gmail.com')
    TestingTools.assert_equal(phone, '289-442-5241')
    TestingTools.assert_equal(website, 'https://github.com/novakivanovski')


def run():
    test_resume()

