"""
shared stuff to keep logging consistent
"""
from constants import PAD
import base64

w = base64.standard_b64encode

def HTTP_MSG(h, name="REQUEST"):
    return "\n\n" + \
           " - %s - ".join([PAD, PAD]) % name + \
           "\n\n" + \
           "\n".join(("%s: %s" % (k, v) for k,v in h.headers.items())) + \
           "\n\n" + \
           h.body + \
           "\n\n"

def PRINT_REQ(request):
    return HTTP_MSG(request)

def PRINT_RES(response):
    return HTTP_MSG(response, name="RESPONSE")
