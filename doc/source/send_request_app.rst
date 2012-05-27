.. _send_request_app:

============
 client_app
============

So far we have seen examples of interacting with :ref:`wsgi
applications <wsgi_application>` as callables to get HTTP Response
messages. And it was mentioned that you would typically interact with
web applications through a web server. 

Wouldn't it be nice if you could interact with web servers in the same
way in your code as you would the :ref:`wsgi applications
<wsgi_application>`, as simple callables? But can you do that? after
all the internet is old, and surely not every website knows how to
communicate via wsgi right? because that's a python
thing.

While you would be right that wsgi is a python thing, and not every
website knows wsgi, if you thought it was impossible, you would be
incorrect. Why is that? Well, it's because though every website may
not understand wsgi, every website does understand HTTP by
definition. If a web server didn't understand HTTP, it wouldnt be a
website. 

So how would you interact with a website? Simple, you use a 
:ref:`wsgi application <wsgi_application>` that takes an HTTP Request message and
sends it out over TCP/IP to the address specified by the url, and then
returns whatever HTTP Response message it is given. 

.. literalinclude:: proxy_usage.py
   :language: python 


And you didn't even have to learn SOAP or WSDL or generate stub code
to do that. NEAT!!!!
