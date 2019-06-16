from Tests import TestingTools


@TestingTools.debug
def construct(database):
    expected_path = r'Storage\config\database.db'
    TestingTools.assert_equal(database.path, expected_path)


@TestingTools.debug
def add_jobs(database):
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
        TestingTools.assert_equal(test_job.listing.title, database_job.listing.title)
        TestingTools.assert_equal(test_job.listing.date, database_job.listing.date)
        TestingTools.assert_equal(test_job.listing.company, database_job.listing.company)
        TestingTools.assert_equal(test_job.listing.location, database_job.listing.location)
        TestingTools.assert_equal(test_job.listing.job_id, database_job.listing.job_id)
        TestingTools.assert_equal(test_job.plaintext, database_job.plaintext)


@TestingTools.timer
def run():
    database = TestingTools.reset_db()
    construct(database)
    add_jobs(database)
