"""
filters for taking care of various aspects of HTTP
"""
from webob import Request
from cookielib import CookieJar
import log as l
import logging


def http_capture_filter(app, callback=lambda request, response: True):
    """
    captures request and response and passes off to a callback

    :rtype: :ref:`wsgi_application`

    :param app: inner :ref:`wsgi_application`

    :param callback: function to call
    """

    def m(environ, start_response):
        request = Request(environ)
        response = request.get_response(app)
        callback(request.copy(), response.copy())
        return response(environ, start_response)
    return m


def http_log_filter(app, level="DEBUG"):
    """
    logs the request and response to the logger http_log at whatever
    level you specify

    :rtype: :ref:`wsgi_application`

    :param app: inner :ref:`wsgi_application`

    :param level: log level
    """
    level_int = getattr(logging, str(level).upper(), None)
    log = logging.getLogger("http_log")
    if level_int == None:
        raise ValueError("level %s is not a valid level" % level)

    def _log_it(request, response):
        log.log(level=level_int, msg=l.PRINT_REQ(request))
        log.log(level=level_int, msg=l.PRINT_RES(response))
    return http_capture_filter(app, callback=_log_it)


def charset_filter(app):
    """
    if charset is missing, set it to a pretty much safe utf8

    :rtype: :ref:`wsgi_application`

    :param app: inner :ref:`wsgi_application`

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

    BUG: for some reason, appengine doesn't respond to this and
    doesn't send gziped when asked.

    :rtype: :ref:`wsgi_application`

    :param app: inner :ref:`wsgi_application`

    """
    def m(environ, start_response):
        request = Request(environ)
        request.accept_encoding = "gzip"
        response = request.get_response(app)
        response.decode_content()
        return response(environ, start_response)
    return m


def assert_filter(app, assert_=lambda request, response: True):
    """
    will allow for assertions to be made on the request and response.

    :rtype: :ref:`wsgi_application`

    :param app: inner :ref:`wsgi_application`

    """
    def m(environ, start_response):
        request = Request(environ)
        response = request.get_response(app)
        assert_(request.copy(), response.copy())
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

    :rtype: :ref:`wsgi_application`

    :param app: inner :ref:`wsgi_application`
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


def auto_redirect_filter(app, limit=10):
    """
    intercepts response, if response.status is redirectish(301, 302)
    will make the next call
    """
    ENV_PATH_KEYS = ("HTTP_HOST",
                     "PATH_INFO",
                     "QUERY_STRING",
                     "REQUEST_METHOD",
                     "SCRIPT_NAME",
                     "SERVER_NAME",
                     "SERVER_PORT",
                     "SERVER_PROTOCOL")

    REDIR_STATUS = [301, 302]
    limit = int(limit)

    def m(environ, start_response):
        count = 1
        request = Request(environ)
        response = request.get_response(app)
        while response.status_int in REDIR_STATUS and count < limit:
            request = Request.blank(response.headers["Location"],
                                    environ={k: v for k, v in request.environ.items() \
                                             if k not in ENV_PATH_KEYS})
            response = request.get_response(app)
            count += 1
        else:
            return response(environ, start_response)
    return m
