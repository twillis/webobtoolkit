============================
 Introduction To Middleware
============================

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

.. _`wsgi`: http://www.wsgi.org
