import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class JobDB(Base):
    __tablename__ = 'Job'
    job_id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    company = Column(String(250), nullable=False)
    location = Column(String(250), nullable=False)
    plaintext = Column(String)


class Database:
    def __init__(self, project_path):
        self.path = os.path.join(project_path, 'Storage', 'config', 'database.db')
        engine = self.get_engine(self.path)
        Base.metadata.create_all(engine)
        self.session = self.get_session(engine)
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
        listing = job.listing
        job_entry = JobDB(job_id=job.get_id(), title=listing.title, date=listing.date,
                          company=listing.company, location=listing.location, plaintext=job.plaintext)
        self.session.add(job_entry)

    def get_jobs(self):
        jobs = self.session.query(JobDB)
        return jobs


