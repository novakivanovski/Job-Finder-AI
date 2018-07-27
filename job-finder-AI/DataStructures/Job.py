class Job:
    def __init__(self, posting):
        self.posting = posting
        self.listing = posting.listing_reference
        self.plaintext = ''
        self.keywords = []
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

    def get_entry_url(self):
        return self.listing.get_url()

    def get_url(self):
        return self.posting.get_url()

    def get_plaintext(self):
        return self.plaintext

    def get_title(self):
        return self.listing.title

    def get_keywords(self):
        return self.keywords

    def set_keywords(self, keywords):
        self.keywords = keywords

    def set_plaintext(self, text):
        self.plaintext = text

    def has_description(self):
        description = self.get_posting_text()
        return description is not None and description is not ''
