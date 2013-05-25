.. webobtoolkit documentation master file, created by
   sphinx-quickstart on Wed Apr 11 09:39:13 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=========================
 Welcome to webobtoolkit
=========================

Webobtoolkit is a set of utilities that can be used to compose HTTP
clients. 


Getting Started with WebObToolKit
=================================

Webob toolkit provides an easy way out of the box to interact with web
sites or wsgi applications. A webob response is returned for every
call so you can leverage your webob knowledge. It may also be useful
for people already familiar with WSGI and WSGI middleware.  

The Client
----------

The webobtoolkit client contains a lot of the typical functionality
you need in an HTTP client. All current HTTP verbs are
supported(GET,POST,PUT,DELETE,OPTIONS,HEAD,...). Each of the methods
takes a url, query string, and an optional assert method and returns a webob Response object.  

getting a response from a website
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's an example of how to get a response from wikipedia.org

.. literalinclude:: responsewiki.py


getting a response from a WSGI application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most python web frameworks provide a way to expose your web
application as a WSGI app, webobtoolkit can interact with WSGI apps
just as if they were running on a web server. This can provide a way
for you to unit test your application without the web server overhead.

.. literalinclude:: responsewsgi.py


As you can see by the example, all you need to do is construct a
client pipeline around your wsgi application. A client pipeline is
merely wsgi middleware that handles things that an HTTP client would
need to handle like cookies and gzip responses.


parameter passing
~~~~~~~~~~~~~~~~~

Often when interacting with websites or wsgi applications you will
need to pass paramters. HTTP provides a couple of ways to do that. One
is via query string.


query string
++++++++++++

The webobtoolkit client can take a query string as either a string or
dictionary like object. Here's an example of using google's ajax
search api.

.. literalinclude:: responseqs.py



form posts
++++++++++

Another way to pass data to a website or wsgi application is through
form posts. This example also shows how you might do an assert on the
response in order to determine how your logic should proceed. 

.. literalinclude:: responsepost.py



upload files
++++++++++++

WebobToolkit also provides a way to programatically upload files. 

.. literalinclude:: responsefiles.py



built ins
~~~~~~~~~

gzip responses
++++++++++++++

some websites return a response that is compressed in order to reduce
bandwidth. By default webobtoolkit can detect and uncompress the
responses automatically for you

cookie support
++++++++++++++

by default webobtoolkit handles cookies and will submit them
automatically as part of subsequent requests.


optional logging
~~~~~~~~~~~~~~~~

The client pipeline has optional logging of both the request and the
response. Here's an example of how to enable it.


Once enabled, the request and the response will be logged at whichever
log level you specificed.

.. literalinclude:: responselogging.py



Contents:

.. toctree::
   :maxdepth: 2

   reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

