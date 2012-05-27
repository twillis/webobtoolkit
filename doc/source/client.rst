======
client
======

by now, hopefully you are somewhat familiar with the wsgi interface
and how webob Request and Response play a role. 

We've seen numerous examples of how small snippets of wsgi middleware
can be composed into a pretty functional application that communicates
via HTTP.

We've also covered how those applications can be hosted by a web
server and then interacted with by web browsers or other clients. 

And finally we saw that any website can be accessed as if it were a
python callable that adheres to the wsgi interface.

WebObToolkit includes a client that you can use for interacting with
wsgi applications and other websites. You can use it to test wsgi
applications or websites, or use it as a means of using services from
those applications or websites in your programs.


.. literalinclude:: client_usage.py
   :language: python

In the above code you see that we are constructing a client_pipeline
to give the client to use. By default it will use
webobtoolkit.client.client_app an instance of
`webobtoolkit.client.client_pipeline <Reference>` which is pre-configured for
cookie support and gzip content decoding.

Reference
=========

.. autofunction:: webobtoolkit.client.client_pipeline

.. autoclass:: webobtoolkit.client.Client
   :members:
