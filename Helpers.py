import requests
from bs4 import BeautifulSoup
import json
import logging


class Helpers:  # refactor this into parser?
    def __init__(self):
        self.tags = ['li', 'p', 'article', 'pre']
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    @staticmethod
    def get_field(text, start_string, end_string):  # get a field from a string, e.g. jobId=abc
        start = text.find(start_string) + len(start_string)
        end = text.find(end_string, start)
        value = text[start:end]
        return value
    
    def generic(self, job):
        soup = BeautifulSoup(job.text, 'html.parser')
        for tag in self.tags:
            instances = soup.find_all(tag)
            for instance in instances:
                job.raw = job.raw + " " + instance.get_text()
        
    def eagle(self, job):
        try:
            r = requests.get(job.url, headers=self.headers)
            job.text = r.text
        except Exception as e:
            job.text = ''
            logging.error(e)
        self.generic(job)

    @staticmethod
    def indeed(job):
        soup = BeautifulSoup(job.text, 'html.parser')
        job.raw = soup.find(id="job_summary").get_text()

    @staticmethod
    def talgroup(job):
        soup = BeautifulSoup(job.text, 'html.parser')
        job.raw = soup.get_text()

    @staticmethod
    def workday(job):
            headers = {'Accept': 'application/json,application/xml'}
            r = requests.get(job.url, headers=headers)
            job.raw = r.json()['openGraphAttributes']['description']

    @staticmethod
    def aerotek(job):
        headers = {'refresh': '0'}
        for i in range(0, 2):
            soup = BeautifulSoup(job.text, 'html.parser')
            try:
                text = soup.find('meta', attrs={'http-equiv': True})['content']
                start = text.find("'")
                end = text.find("'", start + 1)
                job.url = text[start + 1: end - 1]
                r = requests.get(job.url, headers=headers)
                job.text = r.text
            except Exception as e:
                job.text = ''
                logging.error(e)
                
        soup = BeautifulSoup(job.text, 'html.parser')
        job.raw = soup.get_text()

    @staticmethod
    def smoothhiring(job):
        soup = BeautifulSoup(job.text, 'html.parser')
        script_tags = soup.find_all('script')
        start = script_tags[10].text.find('{"id"')
        end = script_tags[10].text.find('};')
        job.raw = script_tags[10].text[start:end+1]

    @staticmethod
    def rbc(job):
        soup = BeautifulSoup(job.text, 'html.parser')
        attrs = {'type': 'text/javascript'}
        raw = soup.find('script', attrs=attrs).get_text()
        start = raw.find('{"status":200')
        end = raw.find(',"flashParams', start)
        json_data = json.loads(raw[start:end])
        job.text = json_data['data']['job']['description'] 
        soup = BeautifulSoup(job.text, 'html.parser')
        job.raw = soup.get_text()

    @staticmethod
    def brassring(job):
        raw = ''
        soup = BeautifulSoup(job.text, 'html.parser')
        text = str(soup.find('input', id='preLoadJSON'))
        start = text.find('{"SmartSearchJSONValue"')
        end = text.find("'/>")
        json_data = json.loads(text[start:end])
        for item in json_data['Jobdetails']['JobDetailQuestions']:
            raw = raw + item['AnswerValue'] + '\n'
        job.raw = BeautifulSoup(raw, 'html.parser').get_text()

    def david_aplin(self, job):
        job_id = self.get_field(job.url, 'rpid=', '&')
        r = requests.get('https://api.aplin.com/jobs/get-job.json?job_id=' + job_id)
        json_txt = json.loads(r.text)['description']
        job.raw = BeautifulSoup(json_txt, 'html.parser').get_text()

    def adp(self, job):
        job_id = self.get_field(job.url, 'jobId=', '&')
        client = self.get_field(job.url, 'client=', '&')
        first_url = 'https://workforcenow.adp.com/jobs/apply/common/careercenter.faces?client=' + client + \
                    '&op=0&locale=en_US&mode=LIVE&access=E&jobId=' + job_id + '6&source=IN&A=N&dojo.preventCache=0'
        second_url = 'https://workforcenow.adp.com/jobs/apply/metaservices/careerCenter/jobDetails/E/en_US?' + \
                     'requisitionOid=' + job_id + '&ccRefId=19000101&client=' + client
        s = requests.Session()
        s.get(first_url)
        r = s.get(second_url)
        text = json.loads(r.text)['data']['description']
        job.raw = BeautifulSoup(text, 'html.parser').get_text()

    @staticmethod
    def jobdiva(job):
        soup = BeautifulSoup(job.text, 'html.parser')
        job.raw = soup.find(class_='job_des').get_text()

    def recruitinginmotion(self, job):
        job_id = self.get_field(job.url, 'b=', '&')
        url = 'https://www2.pcrecruiter.net/pcrbin/jobboard.aspx?action=detail&b=' + job_id + \
              '&src=Indeed&utm_source=Indeed&utm_medium=organic&utm_campaign=Indeed&referrer=&referrer='
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        attrs = {'property': 'og:description'}
        text = soup.find('meta', attrs=attrs)
        job.raw = (text['content'])

    @staticmethod
    def webconnect(job):
        soup = BeautifulSoup(job.text, 'html.parser')
        job.raw = soup.find('span', id='lblDescription').text

    def taleo(self, job):
        search_string = "'descRequisition', "
        start = job.text.find(search_string)
        if start != -1:  # taleo api
            start = start + len(search_string)
            end = job.text.find(']', start) + 1
            job.raw = job.text[start:end]
        else:
            self.generic(job)

    @staticmethod
    def akamai(job):
        link = job.url
        for i in range(4):
            r = requests.get(link, allow_redirects=False)
            link = r.headers['Location']
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        tags = soup.find_all('p', style="margin-top:0px;margin-bottom:0px")
        for tag in tags:
            job.raw = job.raw + tag.text + '\n'
        job.url = link

    def ian_martin(self, job):
        job_id = self.get_field(job.url, '/jobs/', '?')
        url = 'https://public-rest33.bullhornstaffing.com/rest-services/16XNKG/query/JobBoardPost?start=0&count=1&' \
              'where=id=' + job_id + '&fields=id,title,publishedCategory(id,name),address(city,state),employmentType,' \
              'dateLastPublished,publicDescription,isOpen,isPublic,isDeleted'
        r = requests.get(url)
        job.text = json.loads(r.text)['data'][0]['publicDescription']
        job.raw = BeautifulSoup(job.text, 'html.parser').text

    @staticmethod
    def teksystems(job):
        soup = BeautifulSoup(job.text, 'html.parser')
        attrs = {'type': 'application/ld+json'}
        json_text = soup.find('script', attrs=attrs).text
        job.raw = json.loads(json_text)['responsibilities']

    @staticmethod
    def hire_google(job):
        soup = BeautifulSoup(job.text, 'html.parser')
        job.raw = soup.find(class_='bb-jobs-posting__content').text

    def google(self, job):
        attrs = {'type': 'text/javascript'}
        s = requests.Session()
        r = s.get(job.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        tags = soup.find_all('script', attrs=attrs)
        text = tags[1].text
        start = text.find('{')
        end = text.find('}') + 1
        f_text = text[start:end].replace("'", '"')
        f_text = f_text.replace('\\', '\\\\')
        xsrf_token = json.loads(f_text)['xsrfToken']
        js_cache = tags[3]['src']
        cache_url = 'https://careers.google.com' + js_cache
        r = s.get(cache_url)
        r_j = self.get_field(r.text, "'r-j','", "',")
        link = 'https://careers.google.com/jobs/|'
        payload = '7|3|7|' + link + r_j + '|22|' + xsrf_token + '|_|getJobById|4o|1|2|3|4|5|6|1|7|7|Ce9YM_|'
        headers = self.headers
        headers['content-type'] = 'text/x-gwt-rpc; charset=UTF-8'
        headers['origin'] = 'https://careers.google.com'
        headers['x-gwt-permutation'] = js_cache[6:-9]   
        r = s.post('https://careers.google.com/jobs/r-j', headers=headers, data=payload)
        job.raw = r.text

    def get_raw(self, job):
        indeed = job.url.find('ca.indeed.com') != -1
        talgroup = job.url.find('talgroup.net') != -1
        workday = job.url.find('myworkdayjobs.com') != -1
        aerotek = job.url.find('www.aplitrak.com') != -1
        smoothhiring = job.url.find('app.smoothhiring.com') != -1
        rbc = job.url.find('jobs.rbc.com') != -1
        brassring = job.url.find('krb-sjobs.brassring.com') != -1
        eagle = job.url.find('jobs.eagleonline.com') != -1
        taleo = job.url.find('taleo.net') != -1
        david_aplin = job.url.find('www.aplin.com') != -1
        adp = job.url.find('workforcenow.adp.com') != -1
        jobdiva = job.url.find('jobdiva.com') != -1
        recruitinginmotion = job.url.find('recruitinginmotion.com') != -1
        webconnect = job.url.find('webconnect.sendouts.net') != -1
        akamai = job.company.find('Akamai') != -1
        ian_martin = job.url.find('careers.ianmartin.com') != -1
        teksystems = job.url.find('www.teksystems.com') != -1
        hire_google = job.url.find('hire.withgoogle.com') != -1
        google = job.url.find('careers.google.com') != -1
        
        try:
            if eagle:
                self.eagle(job)

            elif aerotek:
                self.aerotek(job)
            
            elif indeed:
                self.indeed(job)

            elif workday:
                self.workday(job)

            elif smoothhiring:
                self.smoothhiring(job)

            elif rbc:
                self.rbc(job)

            elif brassring:
                self.brassring(job)

            elif david_aplin:
                self.david_aplin(job)

            elif talgroup:
                self.talgroup(job)

            elif adp:
                self.adp(job)

            elif jobdiva:
                self.jobdiva(job)

            elif recruitinginmotion:
                self.recruitinginmotion(job)

            elif webconnect:
                self.webconnect(job)

            elif taleo:
                self.taleo(job)

            elif akamai:
                self.akamai(job)

            elif ian_martin:
                self.ian_martin(job)

            elif teksystems:
                self.teksystems(job)

            elif hire_google:
                self.hire_google(job)

            elif google:
                self.google(job)
            
            else:
                self.generic(job)

        except Exception as e:
            logging.error('Error while crawling job posting: ' + str(e))
