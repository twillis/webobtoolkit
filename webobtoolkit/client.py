"""
this is the client api it's mostly sugar
"""
import filters
import proxy
from urllib import urlencode
from webob import Request


def make_client_wsgi(wsgi=proxy.proxy_exact_request,
                     cookie_support=True, content_decoding=True):
    """
    basically wrapping up the app in all the typical stuff you would
    want in a client lib... i think
    """
    if cookie_support:
        wsgi = filters.cookie_filter(wsgi)

    if content_decoding:
        wsgi = filters.decode_filter(wsgi)

    wsgi = filters.charset_filter(wsgi)
    return wsgi


def get(url, params=None, headers=[]):
    app = make_client_wsgi()

    if params and hasattr(params, "keys"):
        params = urlencode(params)
    else:
        params = str(params)

    if headers:
        headers = headers.items()

    return Request.blank(url, method="GET", headers=headers, query_string=params).get_response(app)


def post(url, params=None, data=None, headers=[]):
    app = make_client_wsgi()
    if params and hasattr(params, "keys"):
        params = urlencode(params)
    else:
        params = str(params)

    if headers:
        headers = headers.items()
    return Request.blank(url, method="POST", headers=headers, query_string=params, POST=data).get_response(app)
