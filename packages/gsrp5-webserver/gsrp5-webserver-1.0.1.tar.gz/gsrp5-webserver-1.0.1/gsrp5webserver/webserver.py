# -*- coding: utf-8 -*-
import sys
import os
import ssl
from os.path import join as opj
import logging
from logging.handlers import RotatingFileHandler

import tornado
import tornado.wsgi
import wsgiref.simple_server
from tornado import web, gen, ioloop, escape, httpserver
from tornado.options import define, options, parse_command_line

from optparse import OptionParser
from tools.webconfig import webconfigManager
from tools.webtornado import application,config


if __name__ == "__main__":
	try:
		#print(config['webserver'])
		certs_dir = os.getcwd()
		ssl_ctx = None
		
		if config['webserver']['ssl']:
		    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
		    ssl_ctx.load_cert_chain(os.path.join(certs_dir, config['webserver']['certfile'] ), os.path.join(certs_dir, config['webserver']['keyfile']))
		
		http_server = tornado.httpserver.HTTPServer(application,ssl_options = ssl_ctx)
		http_server.listen(options.port)
		#application.listen(options.port)
		ioloop.IOLoop.current().start()
	except KeyboardInterrupt:
		sys.exit(0)


	
