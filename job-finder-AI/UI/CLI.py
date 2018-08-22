import argparse


class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Command line interface parser.')
        parser.add_argument('-date', help='How far back to search for jobs.')
        parser.add_argument('-title', help='Only search for jobs with this title.')
        parser.add_argument('-site', help='Only search these job sites.')
        args = parser.parse_args()
        print(args)


interface = CLI()