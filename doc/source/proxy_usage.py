"""
proxy_usage.py
"""
from webobtoolkit.proxy import send_request_app
from webob import Request

# let's do a google search and print the response
request = Request.blank("http://www.google.com?q=%s" % "wsgi+as+http+client") 
print request.get_response(send_request_app)


# will print lots of stuff
