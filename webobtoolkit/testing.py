"""
things handy for testing


assert_status_code is a collection of asserts for the HTTP status code
on the response, you can use it like so...


>>> assert_status_code._200(request, response)
"""
from constants import STATUS_CODES
from log import PRINT_REQ, PRINT_RES
from client import Client, client_app
from filters import auto_redirect_filter


def _status_code_err_msg(request, response, expected):
    got = response.status_int

    REQ = PRINT_REQ(request)
    RES = PRINT_RES(response)
    return "Excpected status %s got %s\n\n%s\n\n%s\n\n" % (expected, got, REQ, RES)


def _make_assert_status_code(status=200):
    def c(self, request, response):
        assert response.status_int == status, _status_code_err_msg(request, response, status)
    return c

assert_status_code = type("assert_status_code",
                          (object,),
                          dict([("_%s" % s, _make_assert_status_code(s)) for s in STATUS_CODES]))()


def _200_or_302(request, response):
    valid = [200, 302, 301]
    got = response.status_int
    assert got in valid, _status_code_err_msg(request, response, valid)


def get_assert(status):
    if status:
        try:
            return getattr(assert_status_code, "_%s" % status)
        except AttributeError:  # pragma no cover
            raise ValueError("status %s is not a valid HTTP Status code " \
                             % status)


class TestClient(Client):
    """
    inspired by https://bitbucket.org/ianb/webtest
    basically if anything other than 302 or 200 will result in a failure
    """
    def __init__(self, pipeline=None):
        Client.__init__(self, pipeline=auto_redirect_filter(pipeline or client_app),
                        assert_=_200_or_302)

    def get(self, url, query_string=None, headers={}, status=None):
        kw = dict(query_string=query_string, headers=headers)
        kw["assert_"] = get_assert(status)
        return Client.get(self, url, **kw)

    def head(self, url, query_string=None, headers={}, status=None):
        kw = dict(query_string=query_string, headers=headers)
        kw["assert_"] = get_assert(status)
        return Client.head(self, url, **kw)

    def post(self, url, query_string=None, post={}, headers={}, status=None):
        kw = dict(query_string=query_string, headers=headers, post=post)
        kw["assert_"] = get_assert(status)
        return Client.post(self, url, **kw)

    def put(self, url, query_string=None, post={}, headers={}, status=None):
        kw = dict(query_string=query_string, headers=headers, post=post)
        kw["assert_"] = get_assert(status)
        return Client.put(self, url, **kw)

    def delete(self, url, query_string=None, post={}, headers={}, status=None):
        kw = dict(query_string=query_string, headers=headers, post=post)
        kw["assert_"] = get_assert(status)
        return Client.delete(self, url, **kw)
