"""
this is the client api it's mostly sugar
"""
import filters
import proxy
from urllib import urlencode
from webob import Request


def basic_app(wsgi=proxy.send_request_app,
                     cookie_support=True,
                     content_decoding=True,
                     logging=False, log_level=None):
    """
    basically wrapping up the app in all the typical stuff you would
    want in a client lib... i think
    """
    if content_decoding:
        wsgi = filters.decode_filter(wsgi)

    if logging:
        if log_level:
            wsgi = filters.http_log_filter(wsgi, level=log_level)
        else:
            wsgi = filters.http_log_filter(wsgi)

    if cookie_support:
        wsgi = filters.cookie_filter(wsgi)

    wsgi = filters.charset_filter(wsgi)
    return wsgi


class Client(object):
    """
    app: wsgi application to pass requests to

    assert_: a callback lambda: request, response: True that will be
    called for every call to app
    """

    def __init__(self, app=basic_app(), assert_=None):
        self._app = app
        if assert_:
            self._assert_ = assert_
        else:
            self._assert_ = None

    def get(self, url, query_string=None, headers={}, assert_=None):
        return self(url=url,
                             method="get",
                             query_string=query_string,
                             headers=headers,
                             assert_=assert_)

    def post(self, url, query_string=None, post={}, headers={}, assert_=None):
        return self(url=url,
                             method="post",
                             query_string=query_string,
                             post=post,
                             headers=headers,
                             assert_=assert_)


    def put(self, url, query_string=None, post={}, headers={}, assert_=None):
        return self(url=url,
                             method="put",
                             query_string=query_string,
                             post=post,
                             headers=headers,
                             assert_=assert_)

    def delete(self, url, query_string=None, post={}, headers={}, assert_=None):
        return self(url=url,
                             method="delete",
                             query_string=query_string,
                             post=post,
                             headers=headers,
                             assert_=assert_)

    def __call__(self, url, method="get", query_string=None, post=None, headers={}, assert_=None):
        """
        url: the url for the request

        method: the method for the request

        query_string: the querystring dict which will be urlencoded for you

        post: form post

        headers: extra headers fpr the request

        assert_: a callback to be ran after the response is recieved
        in the form of lambda: request, response: True . If present it
        will be ran for this call only rather than the one set on the
        client

        """
        request = self._make_request(url=url,
                                  method=method,
                                  query_string=query_string,
                                  post=post,
                                  headers=headers)
        response = request.get_response(self._app)

        if assert_:
            assert_(request.copy(), response.copy())
        else:
            if self._assert_:
                self._assert_(request.copy(), response.copy())

        return response

    @classmethod
    def _make_request(self, url, method="get", query_string=None, post=None, headers={}):
        """could be delegated to a request factory"""
        if query_string and hasattr(query_string, "keys"):
            _query_string = urlencode(query_string)
        elif query_string:
            _query_string = str(query_string)
        else:
            _query_string = None

        if headers:
            _headers = headers.items()
        else:
            _headers = None

        return Request.blank(url,
                       method=method.upper(),
                       query_string=_query_string,
                       POST=post,
                       headers=_headers)
