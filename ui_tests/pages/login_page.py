# Create a page class for DemoQA Forms

class FormsPage:
    def __init__(self, page):
        self.page = page
        self.first_name = "#firstName"
        self.last_name = "#lastName"
        self.submit = "#submit"

    def fill_form(self, fname, lname):
        self.page.fill(self.first_name, fname)
        self.page.fill(self.last_name, lname)
        self.page.click(self.submit)