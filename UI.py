from appJar import gui
from Crawler import Crawler
from JobParser import JobParser
from Stats import Stats
from time import sleep
import os
from JobManager import JobManager
import Storage


class UI:
    def on_exit(self):
        pass
        # Kill all threads

    def train_btn(self, value):
        app = self.app
        num_jobs = self.spider.num_jobs
        if value == 'dummy':
            progress = 1
            job_ratio = '1/' + str(num_jobs)
            job = self.spider.jobs[0]

        else:
            self.job_num = self.job_num + 1
            current_job = self.spider.jobs[self.job_num - 1]

            if value == 'Accept':
                current_job.passed = True
            else:
                current_job.passed = False

            if self.job_num >= self.spider.num_jobs:
                app.hideSubWindow("Train")
                self.storage.store_jobs(self.job_manager.jobs)
                return
            
            else:
                job_ratio = str(self.job_num + 1) + '/' + str(num_jobs)
                progress = (self.job_num / num_jobs) * 100
                job = self.spider.jobs[self.job_num]

        title_text = job.title + '\n' + job.company + '\n' + job.location
        app.openSubWindow("Train")
        app.updateListBox('Keywords', job.keywords)
        app.setLabel('job_label', title_text)
        app.setLabelAnchor('job_label', 'center')
        app.setMeter("progress_bar", progress, text=job_ratio + " Jobs")
        app.stopSubWindow()

    def load(self):
        # jobs_percent = 0
        # pages_percent = 0
        extract_percent = 0
        while extract_percent < 100:
            pages_percent = self.spider.percents[0]
            jobs_percent = self.spider.percents[1]
            extract_percent = self.spider.percents[2]
            jobs_percent_text = str(round(jobs_percent, 1)) + '% ' + 'jobs loaded.'
            pages_percent_text = str(round(pages_percent, 1)) + '% ' + 'pages loaded.'
            extract_percent_text = str(round(extract_percent, 1)) + '% ' + 'data extracted.'
            self.app.queueFunction(self.app.setMeter, "pages_bar", pages_percent, text=pages_percent_text)
            self.app.queueFunction(self.app.setMeter, "jobs_bar", jobs_percent, text=jobs_percent_text)
            self.app.queueFunction(self.app.setMeter, "extract_bar", extract_percent, text=extract_percent_text)
            sleep(1)
        self.app.hideSubWindow("LoadScreen")
        
    def press(self, win):
        app = self.app
        if win == 'Setup':
            file_path = self.app.openBox()
            if file_path:
                self.f = JobParser(file_path)
                self.stats = Stats(self.f.keywords)
                self.train_pass = self.storage.train_pass_dir
                self.train_fail = self.storage.train_fail_dir
                self.classify_pass = self.cwd + '\\classify\\pass'
                self.classify_fail = self.cwd + '\\classify\\fail'
                self.storage.create_directory(self.train_pass)
                self.storage.create_directory(self.train_fail)
                self.storage.create_directory(self.classify_pass)
                self.storage.create_directory(self.classify_fail)
                self.storage.clear_directory(self.train_pass)       
                self.storage.clear_directory(self.train_fail)
                self.job_num = 0
                self.num_jobs = 0
                app.showSubWindow("LoadScreen")
                self.spider = Crawler(self.url)
                self.job_manager = JobManager(self.spider)
                app.thread(self.load)
                app.thread(self.job_manager.obtain_jobs())
                self.setup_completed = True
            else:
                app.errorBox("Error.", "No file specified.")
            
        elif win == 'Train':
            if self.setup_completed:
                if self.job_num >= self.num_jobs:
                    self.num_jobs = self.spider.num_jobs
                    self.storage.clear_directory(self.train_pass)
                    self.storage.clear_directory(self.train_fail)
                    self.train_btn('dummy')
                    self.job_num = 0
                app.showSubWindow("Train")
            else:
                app.errorBox("Error.", "Setup not completed.")
            
        else:
            if self.setup_completed:
                training_data = os.listdir(self.train_pass) or os.listdir(self.train_fail)
            else:
                app.errorBox('Error.', 'Setup not completed.')
                return
            
            if training_data:
                self.storage.clear_directory(self.classify_pass)
                self.storage.clear_directory(self.classify_fail)
                self.jobs = self.storage.retrieve_jobs()
                self.stats.clear_training_data()
                self.stats.train(self.jobs)
                for job in self.spider.jobs:
                    job.passed = self.stats.classify(job)
                self.storage.store_jobs(self.job_manager.jobs)
            else:
                app.errorBox("Error.", "No training data found.")

    def about(self):
        message = 'This program finds job postings of interest based on training using keywords.'
        self.app.infoBox("About ML Job Searcher", message, parent=None)

    def settings(self):
        self.app.showSubWindow('Settings')
        
    def __init__(self):
        self.url = "https://www.engineerjobs.com/jobs/software-engineering/canada/ontario/?f="
        self.spider = None
        self.stats = None
        self.storage = Storage.Storage(r'C:\Users\Novak\Documents\projects\Job-Finder-AI')
        self.job_num = 0
        self.num_jobs = 0
        self.job_manager = None
        self.f = None
        self.jobs = []
        self.setup_completed = False
        self.file_path = ''
        self.train_pass = ''
        self.train_fail = ''
        self.classify_pass = ''
        self.classify_fail = ''
        self.cwd = os.getcwd()
        self.app = gui("JobCrawler", "700x300")
        app = self.app
        app.setFont(size=12, family="Arial")
        app.setBg("grey")
        app.setSticky("nsew")
        app.setPadding([20, 60])
        tools = ["ABOUT", "SETTINGS"]
        app.addToolbar(tools, [self.about, self.settings], findIcon=True)
        app.addButton("Setup", self.press, 1, 0)
        app.addButton("Train", self.press, 1, 1)
        app.addButton("Classify", self.press, 1, 2)
        app.startSubWindow("Train", modal=True)
        app.setSize("800x400")
        app.setSticky('ew')
        app.addLabel("job_label", "Job Title", 0, 0, 3)
        app.setSticky('')
        app.addListBox('Keywords', [], 1, 1, 1, 1)
        app.setListBoxWidth('Keywords', 40)
        app.setSticky('e')
        app.addButton('Accept', self.train_btn, 1, 0)
        app.setSticky('w')
        app.addButton('Reject', self.train_btn, 1, 2)
        app.setSticky('ew')
        app.addMeter('progress_bar', 2, 0, 3)
        app.setMeterFill("progress_bar", "grey")
        app.setLabelWidth('job_label', 20)
        app.stopSubWindow()
        app.startSubWindow("Settings", modal=True)
        app.setSize("400x300")
        app.addLabel('time_label', 'Select how many days to use for training.')
        app.addRadioButton("frequency", "1")
        app.addRadioButton("frequency", "3")
        app.addRadioButton("frequency", "7")
        app.addRadioButton("frequency", "14")
        app.addRadioButton("frequency", "30")
        app.stopSubWindow()
        app.startSubWindow("LoadScreen", modal=True)
        app.addLabel('load_label', 'Loading data, please wait...')
        app.setSize("300x200")
        app.setSticky('ew')
        app.addMeter('pages_bar')
        app.setMeterFill("pages_bar", "grey")
        app.addMeter('jobs_bar')
        app.setMeterFill("jobs_bar", "grey")
        app.addMeter('extract_bar')
        app.setMeterFill("extract_bar", "grey")
        app.stopSubWindow()
        app.go()
