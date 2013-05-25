"""
getting a response from wikipedia.org
"""
from webobtoolkit.client import Client
client = Client()
print client.get("http://en.wikipedia.org/wiki/HTTP")
