from BaseHandler import BaseHandler
from lib.db.Page import Page, wiki_key, add_page

import logging

class WikiEditPage(BaseHandler):
    def get(self, page_id):
        if self.user:
            self.render("editpage.html", )
        else:
            self.redirect("/wiki/login")

    def post(self, page_id):
        if not self.user:
            self.redirect('/wiki')

        content = self.request.get('content')

        logging.error("CONTENT %s" % content)

        if content:
            p = Page(parent = wiki_key, content = content)
            page_id = add_page(p)
            self.redirect('/wiki/%s' % page_id)
        else:
            self.render("editpage.html", content = content)