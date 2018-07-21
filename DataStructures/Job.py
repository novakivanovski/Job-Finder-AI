class Job:
    def __init__(self, posting):
        self.posting = posting
        self.listing = posting.listing_reference
        self.keywords = None
        self.raw = None
        self.pased = False

    def get_id(self):
        return self.listing.job_id

    def set_id(self, job_id):
        self.listing.job_id = job_id

    def get_soup(self):
        return self.posting.get_soup()

    def get_posting_text(self):
        return self.posting.get_text()

    def set_description(self, text):
        self.posting.set_plaintext(text)

    def set_url(self, url):
        self.posting.url = url

    def get_entry_url(self):
        return self.listing.url

    def get_url(self):
        return self.posting.url

    def get_raw(self):
        return self.posting.plaintext

    def get_title(self):
        return self.listing.title

    def get_keywords(self):
        return self.posting.keywords

    def set_keywords(self, keywords):
        self.posting.keywords = keywords

    def set_raw(self, text):
        self.posting.plaintext = text

    def has_description(self):
        return self.get_posting_text() is not ''
