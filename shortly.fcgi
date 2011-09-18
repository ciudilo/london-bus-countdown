#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from shortly import create_app 

if __name__ == '__main__':
    application = create_app()
    WSGIServer(application, bindAddress='/tmp/shortly-fcgi.sock').run()
