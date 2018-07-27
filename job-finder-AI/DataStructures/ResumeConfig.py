import json


class ResumeConfig:
    def __init__(self, config_file_path):
        config = self.load_config(config_file_path)
        self.title = config['Title']
        self.email = config['Email']
        self.phone_number = config['Phone']
        self.website = config['Website']
        self.highlights = config['Highlights']
        self.education = config['Education']
        self.projects = config['Projects']
        self.experience = config['Experience']

    @staticmethod
    def load_config(config_file_path):
        with open(config_file_path, 'r') as config_file:
            config_data = config_file.read()
            config_json = json.loads(config_data)
        return config_json


