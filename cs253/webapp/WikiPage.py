from WikiHandler import WikiHandler

class WikiPage(WikiHandler):
    def done(self, page = "", path = ""):
        if page:
            page.render()
            self.render("page.html", page = page, path = path)
        else: 
            self.redirect('/wiki/_edit' + path)