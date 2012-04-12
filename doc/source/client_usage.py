"""
example client usage
"""
from webobtoolkit.client import Client, make_client_wsgi
from webobtoolkit.proxy import proxy_exact_request
import logging
logging.basicConfig(level="DEBUG")

# first we make an application 
app = make_client_wsgi(wsgi=proxy_exact_request, # this wsgi app sends the request to the url you specify
                       cookie_support=True, # turn on cookie support
                       content_decoding=True, # decompress responses if necessary
                       logging=True, # turn on logging
                       log_level="DEBUG") # set log level

client = Client(app=app)

response = client.get("http://www.google.com", params=(dict(q="wsgi as http client")))

assert response.status_int == 200
