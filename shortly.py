#!/usr/bin/python
import os
import urlparse
from parse_countdown import Countdown
from nearest_stop import Stops

from cached_countdown import Countdown
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect

class Shortly(object):

    def __init__(self):
      self.url_map = Map([
        Rule('/shortly/<int:stop_number>', endpoint='get_json'),
        Rule('/shortly/<lat>/<lon>/<limit>', endpoint='get_nearest_stops'),
        Rule('/shortly/', endpoint='get_json'),
		   Rule('/', endpoint='get_json')
      ])
      self.countdown = Countdown()
      self.nearest = Stops()

    def dispatch_request(self, request):
      adapter = self.url_map.bind_to_environ(request.environ)
      try:
        #print 'trying'
        endpoint, values = adapter.match()
	      #print 'matched ' + endpoint + ' '
	      #print values
        return getattr(self, 'on_' + endpoint)(request, **values)
      except HTTPException, e:
        return e;

    def on_get_json(self, request, **stop_number):
      if(len(stop_number) > 0):
        jsonInfo = self.countdown.getCountdownJSON(stop_number['stop_number'])
      else:
        jsonInfo = self.countdown.getCountdownJSON()
      return Response(jsonInfo)
    
    def on_get_nearest_stops(self, request, lat, lon, limit):
      jsonInfo = self.nearest.get_nearest_stops(lat, lon, limit)
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
