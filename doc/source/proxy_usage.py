"""
proxy_usage.py
"""
from webobtoolkit.proxy import proxy_exact_request
from webob import Request

# let's do a google search and print the response
request = Request.blank("http://www.google.com?q=%s" % "wsgi+as+http+client") 
print request.get_response(proxy_exact_request)


# will print lots of stuff
