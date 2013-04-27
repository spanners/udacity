from BaseHandler import BaseHandler
from lib.db.Page import Page

class WikiPage(BaseHandler):
    def get(self, path):

        v = self.request.get('v')
        p = None
        if v:
            if v.isdigit():
                p = Page.by_id(int(v), path)    
            if not p:
                return self.notfound()
        else:
            p = Page.by_path(path).get()

        if p:
            p.render()
            self.render("page.html", page = p, path = path)
        else: 
            self.redirect('/wiki/_edit' + path)