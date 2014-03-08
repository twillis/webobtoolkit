.. WebOb Toolkit documentation master file, created by
   sphinx-quickstart on Sat Mar  8 09:00:00 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

WebOb Toolkit: Requests for Aliens!
===================================

WebOb Toolkit is a tool kit for building HTTP_ clients using WebOb_
request and response objects and `wsgi middleware`_.

You may already be familiar with Webob_ request and response objects
if you have experience with a web framework that uses them such as
pyramid_ or WebTest_ .


Usage
-----

Here are some examples of how WebOb Toolkit can be used.


A Very Simple HTTP Client
~~~~~~~~~~~~~~~~~~~~~~~~~

If you didn't know, WebOb's Request object grew a "get_response_" method for
sending an http request to either a wsgi application, or a url and
returning the response. ::

  >>> from webob import Request
  >>> str(Request.blank("https://google.com").get_response())
  '301 Moved Permanently\nLocation: https://www.google.com/\nContent-Type: text/html; charset=UTF-8\nDate: Sat, 08 Mar 2014 14:58:59 GMT\nExpires: Mon, 07 Apr 2014 14:58:59 GMT\nCache-Control: public, max-age=2592000\nServer: gws\nContent-Length: 220\nX-XSS-Protection: 1; mode=block\nX-Frame-Options: SAMEORIGIN\nAlternate-Protocol: 443:quic\n\n<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">\n<TITLE>301 Moved</TITLE></HEAD><BODY>\n<H1>301 Moved</H1>\nThe document has moved\n<A HREF="https://www.google.com/">here</A>.\r\n</BODY></HTML>\r\n'
  >>> 


That is a pretty neat trick, but as http clients go, typically you
need other functionality like handling `http compression`_ for example
or `handling cookies`_. 

WebOb Toolkit provides this additional functionality as `wsgi
middleware`_ which allows you to compose your own solutions in much
the same way as you compose wsgi applications to be used as HTTP_
Servers.

Handling Compression
~~~~~~~~~~~~~~~~~~~~

According to the `http compression`_ article on wikipedia, an http
client can request a compressed response by including an
"Accept-Encoding" header with the request. In WebOb_ you would
do... ::

  >>> from webob import Request
  >>> Request.blank("https://github.com", headers={"Accept-Encoding": "gzip, deflate"}).get_response().headers.get("Content-Encoding", "Content was not encoded")
  'gzip'
  >>> 

As you can see, we requested gzipped content from github, and it
responded nicely. However, if we were to do anything with the body of
the response we would have to uncompress it first. So, it seems that
the rules for compression is to a header with each request and
uncompress the body of each response if the response includes a
"Content-Encoding" header.


The next example, uses webobtoolkit's decode_filter to handle
compressed responses. ::

  >>> from webob import Request
  >>> from webob.client import send_request_app as app
  >>> from webobtoolkit.filters import decode_filter
  >>> app_gzip = decode_filter(app)
  >>> Request.blank("https://github.com", headers={"Accept-Encoding": "gzip"}).get_response(app).body[:100]
  '\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03\xdd[\xdbr\xe4\xc6\x91}\xf7W\x94\x9b\x1b\xa3\xdd0\xd1\xf7\x1b9M:\xe6B\xd9\xb3\xb6%\xda\x1cY\x92\x1d\x0eF5Ph`\x08\xa0 \\H\xf6\xfc\x98\xdf\xf7\xcb|\xb2\xaa\x00\x14\xd0M69Kk\xbdV\x84\xa6\x9b@]\xb32O\x9e\xcc\xac^\xfd\xf2\xfd\xb7\xef>\xfexy\xc1\x82"\x8e\xce\x7f'
  >>> Request.blank("https://github.com", headers={"Accept-Encoding": "gzip"}).get_response(app_gzip).body[:100]
  '<!DOCTYPE html>\n<html>\n  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http:/'
  >>> 



From the above example you will notice a couple of differences from
previous examples. Firstly we are importing WebOb's send_request_app_
and some `wsgi middleware`_ from webobtoolkit for handling compressed
responses. We wrap webob's app with the decode_filter to create an app
that will decompress any response we may encounter.

The first call to github is through webobs app. And as you can see,
the response is compressed just like we asked. The second call is
through the new app we created by wrapping webob's app with
webobtoolkits decode_filter, and as you can see the response has been
decompressed.

The name "filter" is being used here to differentiate between `wsgi
middleware`_ which is usually used in the context of servers and `wsgi
middleware`_ that is intended for use with clients. Filters and
middleware are identical in regards to how they are implemented.

Here is how the decode_filter is implemented. As you can see, it
doesn't take much to write a filter.

.. literalinclude:: ../../../webobtoolkit/webobtoolkit/filters.py
   :pyobject: decode_filter


A More Robust HTTP Client
~~~~~~~~~~~~~~~~~~~~~~~~~

requests_ is a good example of a more useful http client. According to
the docs it includes a lot of useful things that one would want for in
an http client. Some of the things it includes are.

* handling compression
* handling cookies
* handling redirects
* guessing, handling charset decoding
* connection pooling
* ssl verification
* form posts
* file uploads

And probably much more. 

A lot of this functionality can be written on top of webob and a
series of filters. We've already seen how one might handle
compression. WebOb toolkit provides filters for handling cookies,
redirects and handling unspecified charsets. ::

  >>> from webob import Request
  >>> from webob.client import send_request_app
  >>> from webobtoolkit import filters
  >>> requests_app = filters.auto_redirect_filter(filters.cookie_filter(filters.decode_filter(filters.charset_filter(send_request_app))))
  >>> Request.blank("https://google.com").get_response(requests_app)
  >>> str(Request.blank("https://google.com").get_response(requests_app))[:500]
  '200 OK\nDate: Sat, 08 Mar 2014 17:35:40 GMT\nExpires: -1\nCache-Control: private, max-age=0\nContent-Type: text/html; charset=ISO-8859-1\nServer: gws\nX-XSS-Protection: 1; mode=block\nX-Frame-Options: SAMEORIGIN\n\n<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage"><head><meta content="Search the world\'s information, including webpages, images, videos and more. Google has many special features to help you find exactly what you\'re looking for." name="description"><meta content="noodp" '


We construct requests_app out of a number of filters that are for handling requests and responses.

* if a charset is not specified on the response(which sometimes
  happens), a safe default is chosen in order to reduce the chances
  for decoding errors

* the client advertises support for gzip encoding and decompress the response if necessary
* cookies will be persisted for each response and sent for each request
* if a redirect is encountered follow it automatically.
* form posts are handled by webob already, though some might prefer a better syntax.


Todo
~~~~
* for connection pooling, urllib3 provides an implementation that could be easily used to construct an alternate send_request_app (see: webob.client.SendRequest)
* ssl verification is also provided by urllib3


.. _webob: http://webob.org
.. _wsgi: http://wsgi.org
.. _http: http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol
.. _pyramid: http://docs.pylonsproject.org/en/latest/
.. _webtest: http://webtest.readthedocs.org/en/latest/
.. _get_response: http://docs.webob.org/en/latest/modules/webob.html#webob.request.BaseRequest.get_response
.. _`http compression`: http://en.wikipedia.org/wiki/HTTP_compression
.. _`handling cookies`: http://en.wikipedia.org/wiki/HTTP_cookie
.. _`wsgi middleware`: http://be.groovie.org/2005/10/07/wsgi_and_wsgi_middleware_is_easy.html
.. _send_request_app: http://docs.webob.org/en/latest/modules/client.html#webob.client.send_request_app
.. _requests: http://docs.python-requests.org/en/latest/
