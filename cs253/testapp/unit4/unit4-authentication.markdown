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
	* Name = value pair, e.g.
	** Set-Cookie: user_id = 12345
	* Name is very short
	* Value up to 4kb
* HTTP Request
	* Sent by the browser
	* Name = value pair, separate cookies separated by semicolon e.g.
	** cookie: user_id = 12345; last-seen = Dec 22 1983
	* Don't put semicolons in the cookie!