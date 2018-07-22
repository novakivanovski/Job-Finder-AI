import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Listing(Base):
    __tablename__ = 'Listing'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    company = Column(String(250), nullable=False)
    location = Column(String(250), nullable=False)


class Database:
    def __init__(self, project_path):
        database_path = os.path.join(project_path, 'Storage', 'Database', 'database.db')
        engine = create_engine('sqlite:///' + database_path)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        listing = Listing(id=1, title='Engineer', date='2/4/2018', company='Google', location='Here')
        session.add(listing)
        session.commit()
        q = session.query(Listing)
        for listing in q:
            print(listing.title)
            print(listing.date)
            print(listing.id)
            print(listing.company)
            print(listing.location)
