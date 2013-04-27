from BaseHandler import BaseHandler
from lib.db.Page import Page

class WikiHistoryPage(BaseHandler):
    def get(self, path):
        q = Page.by_path(path)
        q.fetch(limit = 100)

        posts = list(q)
        if posts:
            self.render("wikihistory.html", path = path, posts = posts)
        else:
            self.redirect("/wiki/_edit" + path)