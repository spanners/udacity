from BaseHandler import BaseHandler
from lib.db.Page import Page

class WikiHandler(BaseHandler):
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

        self.done(page = p, path = path)

    def done(self, *a, **kw):
        raise NotImplementedError