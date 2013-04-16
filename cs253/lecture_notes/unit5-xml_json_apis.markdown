# Introduction
We might want our server to make requests to other servers for data, in order to collate/manipulate it for the user's needs.

# How do we make our server talk to other servers?

## urllib2

		>> import urllib2

		>> page = urllib2.urlopen("http://google.com")
		>> contents = page.read()
		>> headers = page.headers.items()
		>> print page.headers['content-type']
		'text/html; charset=ISO-8859-1'

		# take a look at dir(page)

# Why not talk to servers with HTML?

Browsers are very permissive with HTML. It doesn't have to adhere to strict standards in order for browsers to render it, and it is thus sometimes unstructured/error-prone.

This makes parsing HTML for collation/manipulation of data very tricky.

# XML

XML is easier to parse as it has to stick to a structure. Every tag has to have a closing tag. For 'void' tags, you must write a closing slash, like:

		<br />

## Parsing XML

### Document Object Model [DOM].

The internal representation of an XML/HTML Document in the form of a tree.

		>> from xml.dom import minidom

		>> dom = minidom.parseString("<mytag>contents!<children><item>1</item><item>2</item></children></mytag>")
		
		>> print dom.toprettyxml() # (pretty prints structure of xml tree)

		>> print dom.getElementsByTagName("item")[0].childNodes[0].nodeValue
		1

		# look at dir(dom)

# RSS

Stands for RDF Site Summary. RDF stands for: Resource Description Framework.

Resource Description Framework is XML for describing just about anything...

Commonly referred to as "Really Simple Syndication"

# JSON

JavaScript Object Notation. Actually valid JS code :)

Less verbose than XML as you don't need opening and closing tags. It's just a bunch of dictionaries, ala:

	{"key":[1, "two", true, []]}

Use the json module in python:

		>> import json

		>> j = '{"one": 1, "numbers": [1,2,3.5]}'
		>> d = json.loads(j) # now a python dictionary
		>> d['numbers']
		[1, 2, 3.5]
		>> d['one']
		1

## JSON escaping
Make sure to escape quotes in json with a \ so that it doesn't mess up our python parsing!

## Convert to JSON

		>> import json
		>> json.dumps([1,2,3])
		'[1, 2, 3]'

**CAVEAT:** The python version of escaped dumped json uses \\\\", but the valid json uses \"

# How to be a good citizen on the Internet

## Use a good user-agent

* Browser name
* Your name
* Your email address

This allows servers to contact you if you're making too many requests

## Rate-limit yourself.

		import time
		while more:
			get_more()
			time.sleep(1) # pause for one second

Give the server a break!

# Other ways to communicate on the Internet

## SOAP (microsoft)
Urgh. Very very complicated. Invented by Microsoft to make communication on the Internet as complicated as possible. Kinda defines a whole protocol.

## Protocol Buffers (google)
Similar concept to SOAP. Compares to JSON

## Thift (facebook)
Again, compares to JSON

# But just use JSON/XML
Come on. They're common. It makes everyone's lives easier.

# Security
A really big concept, but here's some highlevel summaries

## XSS

        <textarea><script type="javascript">
        send document.cookie() to badguy.com
        do bad stuff
        mwhahahaha pwnd
        </script>
        </textarea>

1. badguy puts a script (as above) in vulnerable website
2. you visit page and badguy fetches your cookies in his site badguy.com
3. badguy can put your cookies in his browser and browse as you!

Shouldn't be a problem if you escape your HTML, or you accept only a safe subset e.g. Markdown

## SQL injection

        db.Gql("SELECT * FROM Link WHERE id = %s") % id

where `id` comes from the URL

This is fine if id is a number, but what if it's the string

        ';--DROP TABLE;

So `%s` allows the user to inject arbitrary SQL into the database.

So you want to make sure you're always providing a wrapper around your SQL.
Google App Engine does this automatically. You can use **SQLAlchemy** which provides
a similar interface. SQLAlchemy also provides ORM (Object Relational Mapping)
which can convert your python objects into SQL, but this is kinda bad as it
disconnects you from the queries you're running. Queries are often what cause
your webapp to be slow, and if you don't have direct control of your queries you
won't be able to scale quite so consistently.

## memcache injection

If you're taking input from the user and are converting that into a cache key,
if memcache isn't validating the key, a user could put something in the URL that
can finish the memcache statement and begin a new one, allowing them to pollute
your cache with stuff.


## CSRF -- Cross-site request forgery
Your trusted site **asciichan.com** has a form action like so:

        <form action="/submit">

Badguy could build a webpage on his own domain, use CSS to hide a form, and
use JavaScript to automatically submit this form on document load like so:

        <form action="http://asciichan.com/submit">

Then you visit badguy's invisible form, your browser will render this form, he'll submit
it for you sneakily, and this will submit to asciichan.com using your cookies on
asciichan.com -- your authorised identity.

Your site Asciichan won't see anything wrong with this -- it will receive a
submission from your IP, using your authorised cookies, but Badguy has just used
this verified identity to perform an action on your behalf.

From Wikipedia https://en.wikipedia.org/wiki/Cross-site_request_forgery :

The following characteristics are common to CSRF:

* Involve sites that rely on a user's identity
* Exploit the site's trust in that identity
* Trick the user's browser into sending HTTP requests to a target site
* Involve HTTP requests that have side effects

A way to prevent this:

Requiring a secret, user-specific token in all form submissions and side-effect
URLs prevents CSRF; the attacker's site cannot put the right token in its
submissions
