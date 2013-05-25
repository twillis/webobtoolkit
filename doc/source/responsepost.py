"""
passing parameters as a form post
"""
from webobtoolkit.client import Client
client = Client()


def assert_success(request, response):
    """
    if response status != 200 then raise an error
    """

    if response.status_int != 200:
        raise Exception("Did not get a valid response from %s" % request.url)


print client.post("http://ajax.googleapis.com/ajax/services/search/web",
                  post=dict(v="1.0", q="define: HTTP"),
                  assert_=assert_success)
