from WikiHandler import WikiHandler

class WikiPage(WikiHandler):
    def done(self, page = "", path = "", age = ""):
        if page:
        	if self.format == "html":
        		self.render("page.html", page = page, path = path, age = age)
        	else:
        		self.render_json(page.as_dict())
        else: 
            self.redirect('/wiki/_edit' + path)