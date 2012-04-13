========
Overview
========

.. _wsgi_overview:

WSGI
====

The official definition is that the `wsgi`_ protocol is the protocol
for a web server and application servers to communicate. `PEP 333`_
describes this protocol in detail. But for most developers all you
really need to know is that it is a low level standard for
programs/processes/objects/ and functions to communicate via `HTTP`_
. If you don't know what `HTTP`_ is, well, use google and read up,
that stuff is important if you are developing web applications.

.. _wsgi_application:

WSGI Application
----------------



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
---------------

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
-------------------------------------------------------------

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



.. _middleware_overview:

Middleware
==========

Now that you know that a :ref:`WSGI application <wsgi_application>` is nothing more than a python
callable/function that takes 2 parameters and returns a list, we need
to cover the concept of middleware. Yet another concept that sounds
enterprisey but it's really simple.

Middleware is a python callable that is given a :ref:`WSGI application
<wsgi_application>` that returns a :ref:`WSGI application
<wsgi_application>`. That's it. 

.. literalinclude:: middleware.py
   :language: python


Let your imagination run wild for a second, think of what you could do
if you could manipulate the HTTP Request message before calling
another application, or think what you could do if you could
manipulate the HTTP Response message before it is returned to the
caller(which could be another function, middleware, or even the
browser).

Here are things that could be good uses for middleware.

  #. log the incoming HTTP Request message and the outgoing HTTP
     Response message
  #. You could replace words in the HTTP Response message body
  #. Add or remove headers from the HTTP Request message or HTTP
     response message.
  #. return a completely fabricated HTTP Response message and not even
     call the inner application

So as you can see, there's some pretty cool things you can do to the
HTTP Request and Response messages in middleware. But, the example
above looks pretty intimidating. 

And we haven't even gotten into any examples of how to manipulate form
input on an HTTP Request message yet because these first few sections
we wanted to emphasize what the interface actually is. 

Unless you are an uber hacker with a lot of time on their hands, or
you are bored, you would likely never write `WSGI applications
<wsgi_application>` or middleware this way. Especially given there are
so many libraries and frameworks that make it easier to do.

Still, like it was stated at the beginning, it is beneficial to know
what's going on because the abstractions will fail you, and when they
do, you need to know what's going on. Heck even WSGI is an abstraction
and it's not without it's faults.

In the next section we cover what webob is, what webob has to do with
wsgi, and what you can do with it. 



.. _webob_overview:

WebOb
=====

If you were to write a significant application using just wsgi,
inevitably you would become intimately familiar with HTTP. If you are
a good software developer, eventually you would come up with your own
representation of a HTTP Request message and a HTTP Response
message given enough time and energy.

You would do this so that all of the little quirks and edge
cases of dealing with HTTP could be held in once place in your code
rather than repeated all over you code base.

Well guess what, likely every web framework in existence has
eventually grown it's own representation of a HTTP Request message
and HTTP Response message, or they used a library such as `webob`_.

The `WebOb`_ library makes it easier for you to deal with wsgi and HTTP
Request and Response messages.

Here's an example of a wsgi application, wsgi middleware and wsgi web
server that we have previously discussed. 

.. literalinclude:: webob_wsgi.py
   :language: python


And `WebOb`_ is well tested, well documented and supports python 2.6
through python 3.x. And thank goodness for the docs, because now if
you have questions on how to use `WebOb`_, you can just go read. :)


.. _`webob`: http://docs.webob.org
.. _`wsgi`: http://www.wsgi.org
.. _`wsgi`: http://www.wsgi.org
.. _`PEP 333`: http://www.python.org/dev/peps/pep-0333
.. _`HTTP`: http://www.w3.org/Protocols/rfc2616/rfc2616.html
.. _`wsgi application`: http://webpython.codepoint.net/wsgi_application_interface


