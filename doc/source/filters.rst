=======================
 webobtololkit Filters
=======================

Filters are a collection of useful(in the authors opinion) :ref:`wsgi
middleware <wsgi_middleware>`, you may find it useful too. 

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

.. literalinclude:: ../../webobtoolkit/filters.py
   :language: python
   :pyobject: charset_filter


decode_filter
=============

.. literalinclude:: ../../webobtoolkit/filters.py
   :language: python
   :pyobject: decode_filter


assert_filter
=============

.. literalinclude:: ../../webobtoolkit/filters.py
   :language: python
   :pyobject: assert_filter


cookiet_filter
==============

.. literalinclude:: ../../webobtoolkit/filters.py
   :language: python
   :pyobject: cookie_filter







