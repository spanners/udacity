from BaseHandler import BaseHandler
from lib.db.Page import Page

import logging

class WikiHistoryPage(BaseHandler):
    def get(self, path):
        if not self.user:
            self.redirect("/wiki/login")

        v = self.request.get('v')
        p = None
        if v:
            if v.isdigit():
                p = Page.by_id(int(v), path)    
            if not p:
                return self.notfound()
        else:
            p = Page.by_path(path).get()

        self.render("editpage.html", path = path, page = p)

        
    def post(self, path):
        if not self.user:
            self.error(400)
            return

        content = self.request.get('content')
        old_page = Page.by_path(path).get()

        if not(old_page or content):
            return
        elif not old_page or old_page.content != content:
            p = Page(parent = Page.parent_key(path), content = content)
            p.put()
            logging.error("CONTENT %s" % content)

        self.redirect('/wiki' + path)