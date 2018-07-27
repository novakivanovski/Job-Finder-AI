class Keyword:
    def __init__(self, name, pass_probability, fail_probability):
        self.name = name
        self.pass_probability = pass_probability
        self.fail_probability = fail_probability

    def clear_probabilities(self):
        self.pass_probability = 0
        self.fail_probability = 0

    def get_name(self):
        return self.name

    def set_pass_probability(self, pass_probability):
        self.pass_probability = pass_probability

    def set_fail_probability(self, fail_probability):
        self.fail_probability = fail_probability

    def get_pass_probability(self):
        return self.pass_probability

    def get_fail_probability(self):
        return self.fail_probability
