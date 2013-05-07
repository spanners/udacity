from datetime import datetime, timedelta

from google.appengine.ext import db
from google.appengine.api import memcache

def age_set(key, val):
    save_time = datetime.utcnow()
    memcache.set(key, (val, save_time))

def age_get(key):
    r = memcache.get(key)
    if r:
        val, save_time = r
        age = (datetime.utcnow() - save_time).total_seconds()
    else:
        val, age = None, 0
    return val, age

def add_page(page):
    page.put()
    get_pages(update = True)
    return str(page.key().id())

def get_pages(update = False):
    mc_key = 'WIKIS'

    pages, age = age_get(mc_key)
    if update or pages is None:
        q = db.GqlQuery("SELECT * "
                        "FROM Page "
                        "WHERE ANCESTOR IS :1 "
                        "ORDER BY created DESC "
                        "LIMIT 10",
                        wiki_key)
        pages = list(q)
        age_set(mc_key, pages)

    return pages, age

def age_str(age):
    s = 'Queried %s seconds ago'
    age = int(age)
    if age == 1:
        s = s.replace('seconds', 'second')
    return s % age

def flush_cache():
    memcache.flush_all()


wiki_key = db.Key.from_path('Wikis', 'wikis')

class Page(db.Model):
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now_add = True)

    @staticmethod
    def parent_key(path):
        return db.Key.from_path('/root' + path, 'pages')

    @classmethod
    def by_path(cls, path):
        q = cls.all()
        q.ancestor(cls.parent_key(path))
        q.order('-created')
        return q

    @classmethod
    def by_id(cls, page_id, path):
        return cls.get_by_id(page_id, cls.parent_key(path))

    def as_dict(self):
        time_fmt = '%c'
        d = {'content': self.content,
             'created': self.created.strftime(time_fmt)}
        return d