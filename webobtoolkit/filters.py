"""
filters for taking care of various aspects of HTTP
"""
from webob import Request
from cookielib import CookieJar


def charset_filter(app):
    """
    if charset is missing, set it to a pretty much safe utf8
    """
    def m(environ, start_response):
        request = Request(environ)
        res = request.get_response(app)
        if not res.charset:
            res.charset = "utf8"
        return res(environ, start_response)
    return m


def decode_filter(app):
    """
    decode the content(in case it's gzipped)
    """
    def m(environ, start_response):
        request = Request(environ)
        response = request.get_response(app)
        response.decode_content()
        return response(environ, start_response)
    return m


class RequestCookieAdapter(object):
    """
    this class merely provides the methods required for a
    cookielib.CookieJar to work on a webob.Request

    potential for yak shaving...very high
    """
    def __init__(self, request):
        self._request = request

    def is_unverifiable(self):
        return True  # sure? Why not?

    def get_full_url(self):
        return self._request.url

    def get_origin_req_host(self):
        return self._request.host

    def add_unredirected_header(self, key, header):
        self._request.headers[key] = header

    def has_header(self, key):
        return key in self._request.headers


class ResponseCookieAdapter(object):
    """
    this class merely provides methods required for a
    cookielib.CookieJar to work on a webob.Response
    """
    def __init__(self, response):
        self._response = response

    def info(self):
        return self

    def getheaders(self, header):
        return self._response.headers.getall(header)


def cookie_filter(app):
    """
    intercepts req/res and keeps track of cookies
    """
    jar = CookieJar()

    def m(environ, start_response):
        request = Request(environ)
        jar.add_cookie_header(RequestCookieAdapter(request))
        response = request.get_response(app)
        cookies = jar.make_cookies(ResponseCookieAdapter(response),
                                   RequestCookieAdapter(request))
        for c in cookies:
            jar.set_cookie(c)

        return response(environ, start_response)
    return m
