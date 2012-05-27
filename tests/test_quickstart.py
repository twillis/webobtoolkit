"""
examples for every example in requests quickstart
http://docs.python-requests.org/en/latest/user/quickstart/
"""
from webob import Request, Response
from webob.client import send_request_app
import urllib
import unittest
import uuid
from cookielib import CookieJar
from webobtoolkit import filters, client, testing
import json
import logging
logging.basicConfig(level="DEBUG")
log = logging.getLogger(__file__)
# these "servers" are simpple wsgi applications that are used for testing
def status_200_server(environ, start_response):
    return Response("OK")(environ, start_response)


def echo_data_server(environ, start_response):
    req = Request(environ)
    return Response(str(req.params))(environ, start_response)


def echo_request_server(environ, start_response):
    req = Request(environ)
    return Response(str(req))(environ, start_response)


def crap_server(environ, start_response):
    response_body = u"I am unicode \u0107".encode("utf-8")
    status = "200 OK"
    headers = [("Content-type", "text/plain"),
               ("Content-Length", len(response_body))]
    start_response(status, headers)
    return [response_body]


def gzip_server(environ, start_response):
    response = Response("this is some text that will be compressed")
    response.encode_content(encoding="gzip")
    return response(environ, start_response)


def cookie_server(environ, start_response):
    request = Request(environ)
    if "the-cookie" in request.cookies:
        return Response(request.cookies["the-cookie"])(environ, start_response)
    else:
        response = Response(body="has your cookie")
        response.set_cookie("the-cookie", str(uuid.uuid4()))
        return response(environ, start_response)


class TestQuickStart(unittest.TestCase):
    def testGet(self):
        r = Request.blank("/").get_response(status_200_server)
        self.assertEqual(r.status_int, 200)

    def testPayload(self):
        """
        urlencoding yourself seems unexpected
        """
        query_string = urllib.urlencode(dict(foo=1, bar=2))
        r = Request.blank("/", query_string=query_string).get_response(echo_data_server)
        self.assertEqual(r.status_int, 200)
        self.assert_("foo" in r.body)
        self.assert_("bar" in r.body)

    def testPayloadPOST(self):
        """
        but POST takes a dict and the param is all caps
        """
        POST = dict(foo=1, bar=2)
        r = Request.blank("/", POST=POST).get_response(echo_data_server)
        self.assertEqual(r.status_int, 200)
        self.assert_("foo" in r.body)
        self.assert_("bar" in r.body)

    def testCharSet(self):
        """
        magically figuring out the charset of the response??
        """
        r = Request.blank("/").get_response(filters.charset_filter(crap_server))
        self.assertEqual(r.status_int, 200)
        self.assert_(r.charset, "no charset")
        self.assert_(r.text)

    def testBinary(self):
        """
        magically figures out transfer encodings and gzip deflates is necessary
        """
        r = Request.blank("/").get_response(filters.decode_filter(gzip_server))
        self.assert_("compressed" in r.body, r.body)

    def testRawResponse(self):
        """
        why would you want to do this if you are using a client lib
        that emphasizes its easy to use?
        """
        pass

    # headers
    def testCustomHeaders(self):
        r = Request.blank("/", headers={"My-Custom-Header": "is rad"}).get_response(echo_request_server)
        self.assert_("My-Custom-Header" in r.body, str(r))

    # cookies
    def testMaintainCookies(self):
        app = filters.cookie_filter(cookie_server)
        r = Request.blank("/").get_response(app)
        self.assert_("the-cookie" in r.headers["set-cookie"], str(r))
        # value = r.cookies["the-cookie"] # cookies not handled the same for request??
        value = r.headers["set-cookie"]
        r2 = Request.blank("/").get_response(app)
        self.assert_(str(r2.body) in value, (value, r2.body))

    def testCookieAdapters(self):
        jar = CookieJar(policy=None)  # DefaultCookiePolicy())

        # set a cookie
        res = Response()
        tstval = str(uuid.uuid4())
        res.set_cookie("a-cookie", tstval, domain="example.com")
        cookies = jar.make_cookies(filters.ResponseCookieAdapter(res),
                                   Request.blank("http://example.com"))
        for c in cookies:
            jar.set_cookie(c)

        self.assert_(len(jar), ("where's my cookies?"))
        self.assert_("a-cookie" in [c.name for c in jar],
                     "seriously, where's my cookie")

        # now put the header on the request please
        request = Request.blank("http://example.com")
        self.assert_(".example.com" in jar._cookies.keys(),
                     jar._cookies.keys())
        jar.add_cookie_header(filters.RequestCookieAdapter(request))
        self.assert_("Cookie" in request.headers,
                     (str(request), "Y NO COOKIES?"))

    def testCustomClient(self):
        pipeline = client.client_pipeline(logging=True, log_level="DEBUG")
        myclient = client.Client(pipeline=pipeline, assert_=testing.assert_status_code._200)

        payload = {'key1': 'value1', 'key2': 'value2'}
        myclient.get("http://httpbin.org/get",
                     query_string=payload)
        myclient.head("http://httpbin.org/get",
                     query_string=payload)

        payload = {'key1': 'value1', 'key2': 'value2'}
        myclient.post("http://httpbin.org/post",
                      post=payload)
        payload = {'key1': 'value1', 'key2': 'value2'}
        myclient.post("http://httpbin.org/post",
                      post=json.dumps(payload))
        payload = {'key1': 'value1', 'key2': 'value2'}
        myclient.put("http://httpbin.org/put",
                     post=json.dumps(payload))

        payload = {'key1': 'value1', 'key2': 'value2'}
        myclient.delete("http://httpbin.org/delete",
                        post=json.dumps(payload))

        myclient.post("http://httpbin.org/post",
                      headers={"content-type": "application/json"},
                      post=json.dumps(payload))

        myclient.get("http://httpbin.org/gzip")
        try:
            myclient.get("http://no")
            self.fail("should have raised an exception")
        except:
            log.debug("yay I got an error", exc_info=True)

        myclient.get("http://no", assert_=testing.assert_status_code._502)

    def testAssertFilter(self):
        nobody = Response(status_int=501)

        def assert_body(request, response):
            assert response.body, "there's no body"
        app = filters.assert_filter(nobody, assert_=assert_body)

        try:
            Request.blank("/").get_response(app)
            self.fail("should have gotten an assertion error")
        except AssertionError:
            pass

        app = filters.assert_filter(Response("I'm somebody"),
                                    assert_=assert_body)
        Request.blank("/").get_response(app)


class TestHoles(unittest.TestCase):
    """
    this doesn't prove anything other than there is 100% test coverage
    """
    def testbasic_app_init(self):
        """
        enable logging with no log_level
        """
        client.client_pipeline(logging=True)

    def testClient_init(self):
        client.Client()

    def testClient_make_request_qs_as_str(self):
        client.Client._make_request("url", query_string="hey hey")

    def testInvalidLogLevel(self):
        """
        should raise value error
        """
        try:
            filters.http_log_filter(client.client_pipeline(), "NO")
            self.fail("no error")
        except ValueError:
            pass
