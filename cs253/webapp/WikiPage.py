from BaseHandler import BaseHandler
from lib.db.Page import age_get, age_set, age_str, wiki_key

from google.appengine.ext import db

class WikiPage(BaseHandler):
    def get(self, page_id):
        page_id = page_id[1:]
        page_key = 'page_' + page_id

        page, age = age_get(page_key)
        if not page:
            key = db.Key.from_path('Page', int(page_id), parent=wiki_key)
            page = db.get(key)
            age_set(page_key, page)
            age = 0

        if not page:
            self.render('editpage.html', content = None)
        elif self.format == 'html':
            self.render("wikilink.html", page = page, age = age_str(age))
        elif self.format == 'json':
            self.render_json(page.as_dict())