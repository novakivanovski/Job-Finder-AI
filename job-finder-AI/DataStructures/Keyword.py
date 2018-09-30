class Keyword:
    def __init__(self, name, pass_count=0, fail_count=0):
        self.name = name
        self.pass_count = pass_count
        self.fail_count = fail_count
        self.pass_probability = 0
        self.fail_probability = 0

    def clear_data(self):
        self.pass_count = 0
        self.fail_count = 0
        self.pass_probability = 0
        self.fail_probability = 0

    def get_name(self):
        return self.name

    def set_pass_probability(self, total_pass_count):
        self.pass_probability = self.pass_count / total_pass_count

    def set_fail_probability(self, total_fail_count):
        self.fail_probability = self.fail_count / total_fail_count

    def get_pass_probability(self):
        return self.pass_probability

    def get_fail_probability(self):
        return self.fail_probability

    def get_pass_count(self):
        return self.pass_count

    def get_fail_count(self):
        return self.fail_count
