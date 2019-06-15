from JobManagers.JobManager import JobManager


class EngineerJobsManager(JobManager):
    def __init__(self, crawler='EngineerJobsCrawler', lister='EngineerJobsLister'):
        super().__init__(crawler, lister)


class IndeedManager(JobManager):
    def __init__(self, crawler='IndeedCrawler', lister='IndeedLister'):
        super().__init__(crawler, lister)


class LinkedInLister(JobManager):
    def __init__(self, crawler='LinkedInCrawler', lister='LinkedInLister'):
        super().__init__(crawler, lister)
