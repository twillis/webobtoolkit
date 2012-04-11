"""
middleware.py
"""


def do_nothing(application):
    def m(environ, start_response):
        # could do something cool here before calling the application
        return application(environ, start_response)
    return m


def do_nothing_2(application):

    def m(environ, start_response):
        #setup someway to capture the inner applications status and
        #headers
        inner_status = None
        inner_headers = []

        def inner_start_response(status, headers):
            inner_status = status
            inner_headers = headers

        # before the application is called
        application_body = application(environ, inner_start_response)

        # could do something after the application is called, but
        # instead we will pass things along
        start_response(inner_status, inner_headers)
        return application_body
    return m
