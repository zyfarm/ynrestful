# -*- coding: utf-8 -*-
__author__ = 'jiyue'

from project.middleware.filters import TracerMiddleware, AuthenticateMiddleware
import falcon
from wsgiref import simple_server
from project.config.meta_config import DEPLOY_MODE
from project.config.utils import ConfigInitor

CONF_FILE_NAME = 'config.ini'

ConfigInitor.config_parser(CONF_FILE_NAME)

api_server = application = falcon.API(middleware=[AuthenticateMiddleware(), TracerMiddleware()])

from project.controllers.basic_restful import BasicApiRouterController

apiRouter = BasicApiRouterController()
api_server.add_route('/meta_api/{service_name}/{version}/{method}/{format}/{sign}/{sign_method}/', apiRouter)

if DEPLOY_MODE.debug == 'True':
    httpd = simple_server.make_server('127.0.0.1', 8000, api_server)
    httpd.serve_forever()
