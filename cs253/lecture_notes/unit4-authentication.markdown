#Auth
##Cookies
A small (< 4kb) piece of data stored in the browser for a website, e.g.

		name = value

or

		user_id = 12345

### How a cookie gets stored

1. Browser makes request to some webservers
2. server sends back in it's response some cookie data in the form of HTTP headers.
3. Browser stores this cookie. The cookie is associated with the website hosted on the server it got the cookie from.
4. Every time your browser makes a request to this website in the future, now it has this cookie, it will send this cookie back to the server.

### Used for...?

* Small pieces of temporary data relevant to a particular user, on this particular browser, right now.

### Limitations

* Generally: 20 cookies per website (up to the browser)
* Length of cookie: < 4kb
* Only for 1 website (i.e udacity.com can only set a cookie for udacity.com)
* Unique

**N.B.** These limitations are all *browser side* enforced, so it's up to the browser to set these limits on cookies. A bug could mean that one or more of these are not respected.

### Cookie Headers

* HTTP Response
	* Sent by the server
	* Name = value pair, e.g. `Set-Cookie: user_id = 12345`
	* Name is very short
	* Value up to 4kb
* HTTP Request
	* Sent by the browser
	* Name = value pair, separate cookies separated by semicolon e.g. Cookie: user_id = 12345; last-seen = Dec 22 1983`
	* **Don't put semicolons in the cookie!**

### A more thorough example of a cookie

		Set-Cookie: USER_ID=12345; expires=Sat, 19-Apr-2014 23:50:21 GMT; path=/; domain=.udacity.com

* expires -- when the cookie will no longer be sent.
* path -- this cookie is relevant to this path (you can restrict cookies to specific paths)
* domain -- specific to sites that end in this domain. Anybody on this domain will receive this cookie.

** NB: the minimum domain you can restrict a cookie to is .reddit.com (if you make it just reddit.com, the '.' automatically gets added)

** NB: You can only set a cookie for that domain or HIGHER, i.e. if I'm at www.reddit.com, I can only set for this or .reddit.com, not foo.reddit.com etc.**

### A command to just get the headers from a url

		$ curl -I www.google.com

		HTTP/1.1 302 Found
		Location: http://www.google.co.uk/
		Cache-Control: private
		Content-Type: text/html; charset=UTF-8
		Set-Cookie: PREF=ID=24c322b9b73e6ebc:FF=0:TM=1365855788:LM=1365855788:S=S41rLCUF8rtOoXg0; expires=Mon, 13-Apr-2015 12:23:08 GMT; path=/; domain=.google.com
		Set-Cookie: NID=67=RMcgCsuqXiSTJZcVK5Z3fFQjJYvC3lrVPivVSIT45RkLGsC-n_DdDi355pRf94XuW1lNhlumuwTY4Zq5vTpXO44zv0CWg1fBrOF6z_ml3CHNbd7ps9ZliSQL6oKfGS5O; expires=Sun, 13-Oct-2013 12:23:08 GMT; path=/; domain=.google.com; HttpOnly
		P3P: CP="This is not a P3P policy! See http://www.google.com/support/accounts/bin/answer.py?hl=en&answer=151657 for more info."
		Date: Sat, 13 Apr 2013 12:23:08 GMT
		Server: gws
		Content-Length: 221
		X-XSS-Protection: 1; mode=block
		X-Frame-Options: SAMEORIGIN


### Another way

Chrome private browsing mode, open debug tools, visit domain, View Headers!

### Testing cookies using Cheating!

You can 'cheat' by editing your cookie in the browser to test some feature

## Hashing

		import hashlib

		x = hashlib.md5("foo!")

		x.hexdigest() # get the hash of x

		# you should use HMAC instead though
		# HMAC is Hash-based Message Authentication Code:

		import hmac
		print hmac.new("secret", "udacity").hexdigest()

### Hashing cookies

		Set-Cookie: visits=5,[hash]

When server requests this cookie again from the browser, we check to see if the rehashed value matches the hash. If it doesn't we know it's been tampered with and we can throw it out.

We do this because the user can cheat too, and fake data.
So we can `hash(SECRET + data)` and check if this matches `[hash]`. 
`SECRET` is a server-side string that we.. keep secret.

### But use bcrypt for passwords. Really.

bcrypt allows you to add a parameter to the hashing function to delay the execution of the function by *n* seconds. This is useful because computers continue to get faster, but we don't want them to be able to bruteforce the hashing algorithm to figure out a mapping from every input string to it's respective hash (i.e. make a rainbow table).
