from BaseHandler import BaseHandler
from Art import Art, art_key, top_arts, gmap_img, get_coords

class Ascii(BaseHandler):
    def render_front(self, title="", art="", error=""):
        arts = top_arts()

        img_url = None
        points = filter(None, (a.coords for a in arts))
        if points:
            img_url = gmap_img(points)

        #display the image URL
        self.render("ascii.html", title = title, art = art, error = error, arts = arts, img_url = img_url)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            p = Art(parent=art_key, title = title, art = art)
            #lookup the user's coordinates from their IP
            coords = get_coords(self.request.remote_addr)
            #if we have coordinates, add them to the art
            if coords:
                    p.coords = coords
            p.put()
            #rerun the query and update the cache
            top_arts(True)

            self.redirect("/ascii")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(error = error, title = title, art =art)
