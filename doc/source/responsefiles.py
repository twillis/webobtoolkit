"""
uploading files example
"""
from webobtoolkit.client import Client, client_pipeline
from webob import Request, Response




def application(environ, start_response):
    """this application merely spits out the keys of the form that was
    posted. we are using webob Request and Response for brevity
    """
    request = Request(environ)
    return Response(str(request.POST.keys()))(environ, start_response)

client = Client(pipeline=client_pipeline(application))
print client.post("/", files=dict(file1=("myfile.txt",
                                    "this is a file containing this text")))
