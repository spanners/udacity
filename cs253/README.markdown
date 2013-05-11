#Udacity CS253


webapp - A Google App Engine web application using webapp2, containing:
* Rot13 -- a form that allows you to ROT13 encode/decode text
* Blog -- a blog with permalinks, using memcached 
* AsciiChan -- a 'chan' style text board with geoip resolution rendered on a static google map image
* Wiki -- a wiki with history, using markdown and memcached

Notes: 

1. Wiki and Blog use the same user accounts, so a login in one persists in the other.
2. You must create your own lib/deploy\_config.py with a secret in order for
   signups to work.
3. *Does not work in windows*. This is because of submodule+symlink hack in
   linux to access a subdirectory within a remote github repo. After git
   clone, to work
   around this, merely delete the **jinja2_markdown** and **markdown** symlinks, and
   rename **j2_md** and **md** to **jinja2_markdown** and **markdown**, respectively
