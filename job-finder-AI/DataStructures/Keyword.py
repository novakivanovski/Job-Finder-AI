class Keyword:
    def __init__(self, name, passed_count, failed_count, total_jobs_passed, total_jobs_failed):
        self.name = name
        self.pass_count = passed_count
        self.fail_count = failed_count
        self.pass_probability = passed_count / total_jobs_passed
        self.fail_probability = failed_count / total_jobs_failed

    def clear_data(self):
        self.pass_count = 0
        self.fail_count = 0
        self.pass_probability = 0
        self.fail_probability = 0

    def get_name(self):
        return self.name

    def get_pass_probability(self):
        return self.pass_probability

    def set_pass_probability(self, total_jobs_passed):
        self.pass_probability = self.pass_count / total_jobs_passed

    def set_fail_probability(self, total_jobs_failed):
        self.fail_probability = self.fail_count / total_jobs_failed

    def get_fail_probability(self):
        return self.fail_probability

    def get_pass_count(self):
        return self.pass_count

    def get_fail_count(self):
        return self.fail_count
