class Job:
    def __init__(self, posting):
        self.posting = posting
        self.listing = posting.listing_reference
        self.plaintext = ''
        self.keyword_names = []
        self.passed = False
        self.score = 0

    def get_id(self):
        return self.listing.job_id

    def set_id(self, job_id):
        self.listing.job_id = job_id

    def get_soup(self):
        return self.posting.get_soup()

    def get_posting_text(self):
        return self.posting.get_text()

    def set_url(self, url):
        self.posting.page.url = url

    def get_listing_url(self):
        return self.listing.get_url()

    def get_posting_url(self):
        return self.posting.get_url()

    def get_plaintext(self):
        return self.plaintext

    def get_title(self):
        return self.listing.title

    def get_keyword_names(self):
        return self.keyword_names

    def set_keyword_names(self, keywords):
        self.keyword_names = keywords

    def set_plaintext(self, text):
        self.plaintext = text

    def set_passed(self, job_passed):
        self.passed = job_passed

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def has_description(self):
        description = self.get_posting_text()
        return description is not None and description is not ''

    def get_location(self):
        return self.listing.location

    def get_company(self):
        return self.listing.company

    def get_date(self):
        return self.listing.date

    def get_passed(self):
        return self.passed


