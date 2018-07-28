from Storage import JobDatabase
import os
from Tests import TestingTools


def delete_db(project_path):
    database_path = os.path.join(project_path, 'Storage', 'config', 'database.db')
    if os.path.isfile(database_path):
        os.unlink(database_path)


def test_constructor(database):
    expected_path = r'C:\Users\n\projects\job-finder-AI\Storage\config\database.db'
    TestingTools.assert_equal(database.path, expected_path)


def test_add_jobs(database):
    test_jobs = []
    test_id = 1337
    test_title = 'Software Engineer'
    test_date = '2/4/2018'
    test_company = 'Google'
    test_location = 'Ontario'
    test_plaintext = 'Test job plaintext'
    test_job1 = TestingTools.get_test_job()
    TestingTools.set_job_parameters(test_job1, job_id=test_id, title=test_title, date=test_date,
                                    company=test_company, location=test_location, plaintext=test_plaintext)
    test_jobs.append(test_job1)
    database.add_jobs(test_jobs)
    database_jobs = database.get_jobs()
    for test_job, database_job in zip(test_jobs, database_jobs):
        TestingTools.assert_equal(test_job.listing.title, database_job.title)
        TestingTools.assert_equal(test_job.listing.date, database_job.date)
        TestingTools.assert_equal(test_job.listing.company, database_job.company)
        TestingTools.assert_equal(test_job.listing.location, database_job.location)
        TestingTools.assert_equal(test_job.listing.job_id, database_job.job_id)
        TestingTools.assert_equal(test_job.plaintext, database_job.plaintext)


def run():
    project_path = os.getcwd()
    delete_db(project_path)
    database = JobDatabase.Database(project_path)
    test_constructor(database)
    test_add_jobs(database)
