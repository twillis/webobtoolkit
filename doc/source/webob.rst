=======================
 Introduction to WebOb
=======================

If you were to write a significant application using just wsgi,
inevitably you would become intimately familiar with HTTP. If you are
a good software developer, eventually you would come up with your own
representation of a HTTP Request message and a HTTP Response
message given enough time and energy.

You would do this so that all of the little quirks and edge
cases of dealing with HTTP could be held in once place in your code
rather than repeated all over you code base.

Well guess what, likely every web framework in existence has
eventually has grown it's own representation of a HTTP Request message
and HTTP Response message, or they used a library such as webob.

The WebOb library makes it easier for you to deal with wsgi and HTTP
Request and Response messages.

Here's an example of a wsgi application, wsgi middleware and wsgi web
server that we have previously discussed. 

.. literalinclude:: webob_wsgi.py
   :language: python


And WebOb is well tested, well documented and supports python 2.6 as
well as python 3.x. And thank goodness for the docs, because now if
you have questions on how to use WebOb, you can just go read. :)
