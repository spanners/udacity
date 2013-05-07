from WikiHandler import WikiHandler

class WikiPage(WikiHandler):
    def done(self, page = "", path = "", age = ""):
        if page:
            self.render("page.html", page = page, path = path, age = age)
        else: 
            self.redirect('/wiki/_edit' + path)