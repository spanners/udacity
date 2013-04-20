from datetime import datetime, timedelta

import logging

from google.appengine.ext import db
from google.appengine.api import memcache

from ..utils import jinja_str

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
    logging.error("DB INSERT")
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
        logging.error("DB QUERY")
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

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return jinja_str("page.html", p = self)

    def as_dict(self):
        time_fmt = '%c'
        d = {'content': self.content,
             'created': self.created.strftime(time_fmt)}
        return d