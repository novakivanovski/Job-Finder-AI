from time import time
from Storage import JobDatabase
import os


def run():
    start = time()
    project_path = os.getcwd()
    database = JobDatabase.Database(project_path)
    elapsed = round((time() - start), 2)
    print('Elapsed time: ' + str(elapsed) + ' seconds')
    print(type(database))

