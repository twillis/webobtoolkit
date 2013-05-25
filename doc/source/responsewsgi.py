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
