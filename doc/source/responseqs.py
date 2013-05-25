"""
passing parameters as a query string
"""
from webobtoolkit.client import Client
client = Client()
result = client.get("http://ajax.googleapis.com/ajax/services/search/web", 
                    query_string=dict(v="1.0", q="define: HTTP")).json
for k, v in result.items():
    print k, ":", v

