#!/usr/bin/env python

from shurl import app as application

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    # httpd.handle_request()
    httpd.serve_forever()


