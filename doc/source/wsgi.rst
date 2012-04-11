======================
 Introduction to WSGI
======================

The official definition is that the `wsgi`_ protocol is the protocol
for a web server and application servers to communicate. `PEP 333`_
describes this protocol in detail. But for most developers all you
really need to know is that it is a low level standard for
programs/processes/objects/ and functions to communicate via `HTTP`_
. If you don't know what `HTTP`_ is, well, use google and read up,
that stuff is important if you are developing web applications.

.. _wsgi_application:

WSGI Application
================



A `wsgi application`_ is an application that implements the `wsgi`_
protocol. Sounds enterprisey doesn't it? It's really quite simple to
implement. It's a callable(or function) that takes 2 parameters and
returns a list.

Here is the simplest `wsgi application`_ you can make.

.. literalinclude:: wsgi_app.py
   :language: python


THAT'S IT!!!!! NO FRAMEWORK NEEDED, other than the standard library. 

Though this application can recieve and return messages that conform
to the `HTTP`_ protocol, this doesn't mean you can now magically point
your web browser at this function and get "Hello World" displayed in
the page. For that you need a :ref:`web_server`. 

.. _web_server:

WSGI Web Server
===============

So what is a web server? it's a application that communicates via `HTTP`_
typically over TCP/IP. We will not cover TCP/IP here. There's plenty
of information elsewhere. What you need to know is that anything that can
communicate via TCP/IP is generally reachable on a port at an IP address. 

So in order to get the above application to be reachable by your web
browser, it needs a web server to listen on a port at a specific IP
address and when an `HTTP`_ Request Message comes in, it would call our
application. 


The python standard library comes with several web servers, but not
all of them can be told to call our application. Here's an example 

.. literalinclude:: wsgi_server.py
   :language: python


Running wsgi_server.py and pointing your browser at
http://localhost:8080 would cause the :ref:`wsgi_application` to spit out a
`HTTP`_ Response Message who's body contains the text "Hello World"


Calling WSGI Application's(they're all just python callables)
===============================================================

Typically a `wsgi application`_ is made available to call over TCPI/IP by
a webserver that knows the `wsgi`_ protocol. But as was stated earlier a
`wsgi application`_ is just a callable that takes 2 parameters and returns
a list (after calling the second parameter "start_response").

So as you may have guessed a `wsgi application`_ can be called just like
any other function or callable if provided the input it
expects. Though calling them this way might be a little more
complicated than necessary for general functions. Still, it is
important to remember that in the end, a `wsgi application`_ is nothing
more than a python callable that you likely use everytime you write
code in python. 

In the rest of the documentation we will show how to exploit the fact
that a `wsgi application`_ is just a python callable, and what cool
things you can do.

.. _`wsgi`: http://www.wsgi.org
.. _`PEP 333`: http://www.python.org/dev/peps/pep-0333
.. _`HTTP`: http://www.w3.org/Protocols/rfc2616/rfc2616.html
.. _`wsgi application`: http://webpython.codepoint.net/wsgi_application_interface
