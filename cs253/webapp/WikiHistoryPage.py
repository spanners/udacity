from BaseHandler import BaseHandler
from lib.db.Page import get_pages

#import logging

class WikiHistoryPage(BaseHandler):
    def get(self, path):
        pages, age = get_pages(path)

        if pages:
        	#logging.error("PS Used Memcached")
        	self.render("wikihistory.html", path = path, pages = pages)
        else:
            self.redirect("/wiki/_edit" + path)