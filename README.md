#  WebobToolkit

WebobToolKit is a set of utilities that can be used to compose HTTP
clients built on top of [Webob](http://docs.webob.org/en/latest/reference.html).

## Getting Started

WebobToolKit provides an easy way out of the box to interact with web
sites or [wsgi](http://wsgi.readthedocs.org/en/latest/)
applications. A [webob response](http://docs.webob.org/en/latest/reference.html#id2) is
returned for every call so you can leverage your webob knowledge. It
may also be useful for people already familiar with WSGI and [WSGI
middleware](http://docs.webob.org/en/latest/comment-example.html#id5).

### The Client

The WebobToolKit client contains a lot of the typical functionality
you need in an HTTP client. All current HTTP verbs are
supported(GET,POST,PUT,DELETE,OPTIONS,HEAD,...). Each of the methods
takes a URL, query string, and an optional assert method and returns a
webob Response object.

#### Getting a Response from a Website

Here’s an example of how to get a response from wikipedia.org

```python
"""
getting a response from wikipedia.org
"""
from webobtoolkit.client import Client
client = Client()
print client.get("http://en.wikipedia.org/wiki/HTTP")
```

#### Getting a Response from a WSGI Application

Most python web frameworks provide a way to expose your web
application as a WSGI app, WebobToolKit can interact with WSGI apps
just as if they were running on a web server. This can provide a way
for you to unit test your application without the web server overhead.

As you can see from the example below, all you need to do is construct
a client pipeline around your wsgi application. A client pipeline is
merely wsgi middleware that handles things that an HTTP client would
need to handle like cookies and gzip responses.

```python
"""
getting a response from a wsgi application
"""
from webobtoolkit import client


def application(environ, start_response):
    """
    most python webframeworks provide a way to expose your web
    application as a WSGI app. consult your framework documentation
    for details.
    """
    status = "200 OK"  # HTTP messages have a status
    body = "Hello World"  # HTTP messages have a body

    # HTTP messages have headers to describe various things, at a
    # minimum describing the type(Content-Type) and the length of the
    # content(Content-Length)
    headers = [("Content-Type", "text/plain"),
               ("Content-Length",
                str(len(body)))]

    start_response(status, headers)  # calling the function passed in
                                     # with the status and headers of
                                     # the HTTP Response Message

    return [body]  # returning a list containing the body of the HTTP
                   # Response Message

print client.Client(pipeline=client.client_pipeline(application)).get("/")
```


#### Parameter Passing

Often when interacting with websites or wsgi applications you will
need to pass parameters. HTTP provides a couple of ways to do that. One
is via query string.


##### Query String

The webobtoolkit client can take a query string as either a string or
dictionary like object. Here’s an example of using Google’s ajax
search api.

```python
"""
passing parameters as a query string
"""
from webobtoolkit.client import Client
client = Client()
result = client.get("http://ajax.googleapis.com/ajax/services/search/web", 
                    query_string=dict(v="1.0", q="define: HTTP")).json
for k, v in result.items():
    print k, ":", v
```


##### Form Posts

Another way to pass data to a website or wsgi application is through
form posts. This example also shows how you might do an assert on the
response in order to determine how your logic should proceed.

```python
"""
passing parameters as a form post
"""
from webobtoolkit.client import Client
client = Client()


def assert_success(request, response):
    """
    if response status != 200 then raise an error
    """

    if response.status_int != 200:
        raise Exception("Did not get a valid response from %s" % request.url)


print client.post("http://ajax.googleapis.com/ajax/services/search/web",
                  post=dict(v="1.0", q="define: HTTP"),
                  assert_=assert_success)
```

##### Upload Files

WebobToolkit also provides a way to programmaticly upload files.

```python

"""
uploading files example
"""
from webobtoolkit.client import Client, client_pipeline
from webob import Request, Response




def application(environ, start_response):
    """this application merely spits out the keys of the form that was
    posted. we are using webob Request and Response for brevity
    """
    request = Request(environ)
    return Response(str(request.POST.keys()))(environ, start_response)

client = Client(pipeline=client_pipeline(application))
print client.post("/", files=dict(file1=("myfile.txt",
                                    "this is a file containing this text")))
```


#### Built-ins

Some of the intricacies of HTTP are handled automatically for you.

##### Gzipped Responses

Some websites return a response that is compressed in order to reduce
bandwidth. By default WebobToolKit can detect and un-compress the
responses automatically for you

##### Cookie Support

By default WebobToolKit handles cookies and will submit them
automatically as part of subsequent requests.

#### Optional Logging

The client pipeline has optional logging of both the request and the
response. Here’s an example of how to enable it.


Once enabled, the request and the response will be logged at whichever
log level you specified.


```python
"""
enable logging of request and response
"""
from webobtoolkit import client
import logging
logging.basicConfig(level=logging.DEBUG)

c = client.Client(client.client_pipeline(logging=True, log_level=logging.DEBUG))
c.get("http://google.com")
```
