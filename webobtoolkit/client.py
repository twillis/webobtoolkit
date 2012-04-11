"""
this is the client api it's mostly sugar
"""
import filters
import proxy
from urllib import urlencode
from webob import Request


def make_client_wsgi(wsgi=proxy.proxy_exact_request,
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

    def __init__(self, app=make_client_wsgi(), assert_=None):
        self._app = app
        if assert_:
            self._assert_ = assert_
        else:
            self._assert_ = None

    def get(self, url, params=None, headers={}, assert_=None):
        return self.__call__(url=url, method="get", params=params, headers=headers, assert_=assert_)

    def post(self, url, params=None, data={}, headers={}, assert_=None):
        return self.__call__(url=url, method="post", params=params, data=data, headers=headers, assert_=assert_)


    def put(self, url, params=None, data={}, headers={}, assert_=None):
        return self.__call__(url=url, method="put", params=params, data=data, headers=headers, assert_=assert_)

    def delete(self, url, params=None, data={}, headers={}, assert_=None):
        return self.__call__(url=url, method="delete", params=params, data=data, headers=headers, assert_=assert_)

    def __call__(self, url, method="get", params=None, data=None, headers={}, assert_=None):
        """
        url: the url for the request

        method: the method for the request

        params: the querystring dict which will be urlencoded for you

        data: form post

        headers: extra headers fpr the request

        assert_: a callback to be ran after the response is recieved
        in the form of lambda: request, response: True

        """
        request = self._make_request(url=url,
                                  method=method,
                                  params=params,
                                  data=data,
                                  headers=headers)
        response = request.get_response(self._app)

        if assert_:
            assert_(request.copy(), response.copy())
        else:
            if self._assert_:
                self._assert_(request, response)

        return response

    @classmethod
    def _make_request(self, url, method="get", params=None, data=None, headers={}):
        """could be delegated to a request factory"""
        if params and hasattr(params, "keys"):
            _params = urlencode(params)
        elif params:
            _params = str(params)
        else:
            _params = None

        if headers:
            _headers = headers.items()
        else:
            _headers = None

        return Request.blank(url,
                       method=method.upper(),
                       query_string=_params,
                       POST=data,
                       headers=_headers)
