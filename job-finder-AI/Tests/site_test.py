from Storage.LocalStorage import LocalStorage
from UI import Site


def run():
    Site.app.run()


@Site.app.route('/sandbox')
def sandbox():
    storage = LocalStorage()
    jobs = storage.get_jobs_from_database()
    titles = '\r\n'.join([job.get_title() for job in jobs])
    return titles
