"""
example client usage
"""
from webobtoolkit.client import Client, client_pipeline
from webobtoolkit.proxy import send_request_app
import logging
logging.basicConfig(level="DEBUG")

# first we make an pipeline 
pipeline = client_pipeline(wsgi=send_request_app, # this wsgi app sends the request to the url you specify
                       cookie_support=True, # turn on cookie support
                       content_decoding=True, # decompress responses if necessary
                       logging=True, # turn on logging
                       log_level="DEBUG") # set log level

client = Client(pipeline=pipeline)

response = client.get("http://www.google.com", query_string=(dict(q="wsgi as http client")))

assert response.status_int == 200, "something went wrong"
