"""
wsgi_server.py
"""
from wsgi_app import application
from wsgiref.simple_server import make_server

 # listen on the local address so that it's only reachable by the
 # machine it's running on. on port 8080, when a HTTP Request is
 # recieved, call application(environ, start_response)
server = make_server("localhost", 8080, application)

# after you recieve one HTTP Request, handle it than quit.
server.handle_request()
