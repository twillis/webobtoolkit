"""
client usage
"""
from webob import Request
from webobtoolkit.client import client_app
# let's do a google search and print the response
request = Request.blank("http://www.google.com?q=%s" % "wsgi+as+http+client") 
print str(request.send())
# or
print str(request.send(client_app) # for cookie support, content decoding support

# will print lots of stuff
