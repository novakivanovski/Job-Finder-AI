import os
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataStructures.Listing import Listing
from DataStructures.Posting import Posting
from DataStructures.Page import Page
from DataStructures.Job import Job
from Utilities.ApplicationExceptions import DatabaseError

Base = declarative_base()


class JobTable(Base):
    __tablename__ = 'JobTable'
    job_id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(String)
    location = Column(String)
    company = Column(String)
    listing_url = Column(String)
    posting_url = Column(String)
    posting_html = Column(String)
    plaintext = Column(String)
    keywords = Column(String)
    passed = Column(Boolean)


class JobDatabase:
    def __init__(self):
        self.path = os.path.join('Storage', 'config', 'database.db')
        self.engine = self.get_engine(self.path)
        Base.metadata.create_all(self.engine)
        self.session = self.get_session(self.engine)
        self.job_table = self.session.query(JobTable)
        self.session.commit()

    @staticmethod
    def get_session(engine):
        sesh = sessionmaker(bind=engine)
        session = sesh()
        return session

    @staticmethod
    def get_engine(path):
        engine = create_engine('sqlite:///' + path)
        return engine

    def add_jobs(self, jobs):
        for job in jobs:
            self.add_job(job)
        self.session.commit()

    def add_job(self, job):
        job_entry = JobTable(job_id=job.get_id(), title=job.get_title(), date=job.get_date(),
                             location=job.get_location(), company=job.get_company(), listing_url=job.get_listing_url(),
                             posting_html=job.get_posting_text(), posting_url=job.get_posting_url(),
                             plaintext=job.get_plaintext(), keywords=', '.join(job.get_keyword_names()),
                             passed=job.passed)
        self.session.add(job_entry)

    def get_jobs(self):
        jobs = []
        for job_entry in self.job_table:
            job = self.convert_entry_to_job(job_entry)
            jobs.append(job)
        return jobs

    @staticmethod
    def convert_entry_to_job(job_entry):
        try:
            listing = Listing(job_entry.title, job_entry.date, job_entry.location,
                              job_entry.company, job_entry.listing_url, job_entry.job_id)
            posting_page = Page(job_entry.posting_html, job_entry.posting_url)
            posting = Posting(listing, posting_page)
            job = Job(posting)
            job.set_plaintext(job_entry.plaintext)
            job.set_keyword_names(job_entry.keywords.split(', '))
            job.set_passed(job_entry.passed)
        except Exception as e:
            raise DatabaseError('Error: Unable to convert listing to job: ' + str(e))
        return job

    def get_last_id(self):
        statement = 'SELECT MAX(job_id) FROM JobTable'
        result = self.session.execute(statement)
        last_id = result.fetchone()[0]
        self.session.commit()
        return last_id if last_id else 0

    def update_entry(self, job):
        job_entry = self.session.query(JobTable).filter_by(job_id=job.get_id()).first()
        job_entry.passed = job.get_passed()
        self.session.commit()

    def close(self):
        self.session.close()






