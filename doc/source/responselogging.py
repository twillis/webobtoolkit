"""
enable logging of request and response
"""
from webobtoolkit import client
import logging
logging.basicConfig(level=logging.DEBUG)

c = client.Client(client.client_pipeline(logging=True, log_level=logging.DEBUG))
c.get("http://google.com")
