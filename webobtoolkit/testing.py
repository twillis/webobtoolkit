"""
things handy for testing


assert_status_code is a collection of asserts for the HTTP status code
on the response, you can use it like so...


>>> assert_status_code._200(request, response)
"""
from constants import STATUS_CODES
from log import PRINT_REQ, PRINT_RES



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
