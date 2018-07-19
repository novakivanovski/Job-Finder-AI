import sqlalchemy
import os

# Use SQLite database engine.


class Database:
    def __init__(self, project_path):
        self.database_directory = os.path.join(project_path, 'Storage', 'Job Database')
        print(sqlalchemy.__version__)
        print(self.database_directory)


db = Database(r'C:\Users\Novak\projects\Job-Finder-AI')
