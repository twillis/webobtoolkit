"""
shared stuff to keep logging consistent
"""
from constants import PAD


def HTTP_MSG(h):
    if hasattr(h, "method"):
        hdr = "%s %s %s" % (h.method, h.path, h.http_version)
        name = "REQUEST"
    else:
        hdr = h.status
        name = "RESPONSE"
    return "\n\n" + \
           " - %s - ".join([PAD, PAD]) % name + \
           "\n\n" + \
           "%s\n" % hdr + \
           "\n".join(("%s: %s" % (k, v) for k, v in h.headers.items())) + \
           "\n\n" + \
           h.body + \
           "\n\n"


def PRINT_REQ(request):
    return HTTP_MSG(request)


def PRINT_RES(response):
    return HTTP_MSG(response)
