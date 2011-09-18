import os
import urlparse
from parse_countdown import Countdown
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader

class Shortly(object):

    def __init__(self):
      self.url_map = Map([
        Rule('/<stop_number>', endpoint='get_json'),
      ])

    def dispatch_request(self, request):
	jsonInfo = Countdown().getCountdownJSON()
	print jsonInfo
	return Response(jsonInfo)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(with_static=True):
    app = Shortly()
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 8080, app, use_debugger=True, use_reloader=True)
