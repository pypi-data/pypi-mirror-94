import tornado
import tornado.web
import tornado.wsgi
import wsgiref.simple_server
from tools.webtornado import application

wsgi_app = tornado.wsgi.WSGIAdapter(application)
server = wsgiref.simple_server.make_server('', 8888, wsgi_app)
server.serve_forever()

