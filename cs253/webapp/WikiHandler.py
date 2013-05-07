from BaseHandler import BaseHandler
from lib.db.Page import Page, age_get, age_set, age_str

class WikiHandler(BaseHandler):
    def get(self, path):
        v = self.request.get('v')
        p = None
        age = None
        if v:
            if v.isdigit():
                page_key = 'PAGE_' + path + v

                p, age = age_get(page_key)

                if not p:
                    p = Page.by_id(int(v), path)
                    age_set(page_key, p)
                    age = 0

            if not p:
                return self.notfound()
        else:
            page_key = 'PAGE_' + path

            p, age = age_get(page_key)

            if not p:
                p = Page.by_path(path).get()
                age_set(page_key, p)
                age = 0

        self.done(page = p, path = path, age = age_str(age))

    def done(self, *a, **kw):
        raise NotImplementedError