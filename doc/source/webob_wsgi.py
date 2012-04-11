"""
webob_wsgi.py
"""
from webob import Request, Response
from wsgiref.simple_server import make_server


def wsgi_hello_app(environ, start_response):
    response = Response("Hello World")

    #did you know that Response is a wsgi application
    return response(environ, start_response)

# or this one-liner, because Response is a wsgi application
wsgi_hello_app = Response("Hello World")


def wsgi_hello_middleware(app):
    def m(environ, start_response):
        request = Request(environ)

        # request is a lot easier to manipulate than a dictionary
        # let's add a header to prove a point
        request.headers["WSGI-Hello-Middleware"] = "Say Hello Application"

        # call a wsgi app and convert what it returns into a
        # webob.Response which is easier to manipulate
        response = request.get_response(app)

        response.headers["WSGI-Application-Middleware"] = "Say Hello Caller"
        return response(environ, start_response)
    return m


application = wsgi_hello_middleware(wsgi_hello_app)
server = make_server("localhost", 8080, application)
server.handle_request()
