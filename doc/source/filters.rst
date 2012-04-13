=======
Filters
=======

Filters are a collection of useful(in the authors opinion) :ref:`wsgi
middleware <middleware_overview>` that is more client-centric than
server-centric, you may find it useful too.

http_capture_filter
===================

this filter captures the request and response and calls a function you
provide so that you can do what you will. it's important to note that
the request and response you recieve are copies and modifying them
does not effect the request or the response going to the application
or client. 

It is primarily user be the :ref:`http_log_filter`

.. literalinclude:: ../../webobtoolkit/filters.py
   :language: python
   :pyobject: http_capture_filter


.. _http_log_filter:

http_log_filter
===============

The http_log_filter will log both the request and the response to the
log_level you provide. The default level is "DEBUG", it's handy when
you need to see what the http traffic looks like in your application,
but using it in production would insure you have huge log files that
you would likely never read.

.. literalinclude:: ../../webobtoolkit/filters.py
   :language: python
   :pyobject: http_log_filter


charset_filter
==============

Some websites won't specify a charset on the response, this can
sometimes be problematic. this filter will check if the charset
attribute is set, and if it isn't it will set it to utf8 which is a
pretty safe bet in most cases. 

.. TODO: this doesn't seem really useful

.. literalinclude:: ../../webobtoolkit/filters.py
   :language: python
   :pyobject: charset_filter


.. _decode_filter:

decode_filter
=============

Websites can return compressed responses. This filter will handle
de-compressing them if a compressed response is detected.

.. literalinclude:: ../../webobtoolkit/filters.py
   :language: python
   :pyobject: decode_filter


.. _assert_filter:

assert_filter
=============

Sometimes you want to raise an error if you get a response under
certain conditions. This filter allows you to specify a function to do
that assertion before the response is returned. The function you
specify will be passed a copy of the request and response.

.. TODO: should this depend on :ref:`http_capture_filter` and should
.. the assert_ just be called condition?

.. literalinclude:: ../../webobtoolkit/filters.py
   :language: python
   :pyobject: assert_filter



.. _cookie_filter:

cookie_filter
==============

Sometime when you are communicating with :ref:`wsgi applications
<wsgi_application>` over several requests, you need to handle the
cookies in order for the application to respond correctly, for example
if you have to login before doing anything else. This filter handles
all the gory details of cookie handling for you.

.. literalinclude:: ../../webobtoolkit/filters.py
   :language: python
   :pyobject: cookie_filter


Usage
=====

Filters can be combined to suit your needs. For example you could
compose a :ref:`wsgi application <wsgi_application>` to support
:ref:`cookies <cookie_filter>` and :ref:`compressed responses
<decode_filter>` and :ref:`raise an error <assert_filter>` if the
inner application responds with a status code of "401", which means
access denied.


.. literalinclude:: filter_usage.py
   :language: python


Reference
=========

.. automodule:: webobtoolkit.filters
   :members:
