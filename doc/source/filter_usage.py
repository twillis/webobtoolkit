"""
using filters
"""
from webobtoolkit import filters
from webob import Request, Response
import datetime


def time_application(environ, start_response):
    body = "the current time is %s " % datetime.datetime.now().isoformat()
    return Response(body)(environ, start_response)


# add cookie support
application = filters.cookie_filter(time_application)

# decompress the response if it is compressed
application = filters.decode_filter(time_application)


# raise an error the app returns something other than a 200 success
# response
def assert_success(request, response):
    assert response.status_int == 200, "the request was not sucessful"


application = filters.assert_filter(time_application, assert_=assert_success)

response = Request.blank("/").get_response(application)

print str(response)
