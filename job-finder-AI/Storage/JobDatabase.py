import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = 'UserProfile'
    username = Column(String(12), primary_key=True)
    password = Column(String(16), nullable=False)
    settings = Column(String, nullable=True)


class JobDB(Base):
    __tablename__ = 'Job'
    job_id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    company = Column(String(250), nullable=False)
    location = Column(String(250), nullable=False)
    plaintext = Column(String)


class JobDatabase:
    def __init__(self):
        self.path = os.path.join('Storage', 'config', 'database.db')
        self.engine = self.get_engine(self.path)
        Base.metadata.create_all(self.engine)
        self.session = self.get_session(self.engine)
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

    def get_last_id(self):
        statement = 'SELECT MAX(job_id) FROM Job'
        result = self.session.execute(statement)
        last_id = result.fetchone()[0]
        return last_id if last_id else 0


