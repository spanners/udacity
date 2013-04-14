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

Browsers are very permissive with HTML. It doesn't have to adhere to strict standards in order for browsers to render it, and it is thus somemtimes unstructured/error-prone.

This makes parsing HTML for collation/maniupulation of data very tricky.

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