# -*- coding: utf-8 -*-

import logging
from project.config.routes import registed_services
from project.decorators.wrapper_response import ApiDecorator

__author__ = 'jiyue'


class BasicApiRouterController:
    u'基本的api路由控制转发类'

    def __init__(self):
        self.logger = logging.getLogger('main.metaservice')

    @ApiDecorator.response_wrapper
    def on_get(self, req, resp, sys_params, app_params):
        self.logger.info("sys_params:%s,app_params:%s", sys_params, app_params)
        service = registed_services[sys_params['service_name']]
        obj_func = getattr(service, sys_params['method'])

        data = apply(obj_func, [], app_params)
        return data
