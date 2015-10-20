import json
import logging
import falcon
import jsonpickle
from project.config.utils import ConfigInitor

from project.utils.mix_tools import sql_alchemy_to_json_encoder

__author__ = 'jiyue'


class ApiDecorator(object):
    redis_proxy = ConfigInitor.redis_client

    def __init__(self):
        self.logger = logging.getLogger('api_decorator')

    @staticmethod
    def cache_wrapper(method):
        def response_from_cache(*args, **kwargs):
            pass

    @staticmethod
    def checkApiExist(routeConfig):
        from project.config.routes import registed_services

        if False == registed_services.has_key(routeConfig['service_name']) \
                or False == hasattr(registed_services[routeConfig['service_name']], routeConfig['method']):
            raise falcon.HTTPNotFound()

    @staticmethod
    def sql_alchemy_json_serilizer(filted_fields):
        def return_json_filter(method):
            def return_json(*args, **kwargs):
                data = method(args[0], **kwargs)
                res = json.loads(json.dumps(data, cls=sql_alchemy_to_json_encoder(), check_circular=False))
                for field in filted_fields:
                    if res.has_key(field):
                        del res[field]
                return res

            return return_json

        return return_json_filter

    @staticmethod
    def response_wrapper(method):
        def response_service(*args, **kwargs):
            routeConfig = {}
            routeConfig['service_name'] = kwargs['service_name']
            routeConfig['method'] = kwargs['method']
            routeConfig['version'] = 'v0' if None == kwargs['version'] else 'v0'
            routeConfig['sign'] = 'dummy' if None == kwargs['sign'] else kwargs['sign']
            routeConfig['sign_method'] = 'dummy' if None == kwargs['sign'] else kwargs['sign']
            routeConfig['format'] = 'json' if None == kwargs['format'] else kwargs['format']

            ApiDecorator.checkApiExist(routeConfig)
            kwargs['service_name'] = routeConfig['service_name']
            kwargs['method'] = routeConfig['method']

            req = args[1]
            res = args[2]

            app_params = req.params
            res.status = falcon.HTTP_200
            try:
                data = method(args[0], req, res, kwargs, app_params)
                res_data = {}
                res_data['status'] = 200
                res_data['errCode'] = 0
                res_data['errMsg'] = 'success'
                res_data['data'] = json.loads(jsonpickle.encode(data, False, False))
                res_data['rid'] = req.params['rid']
                res.body = json.dumps(res_data)

            except falcon.HTTPNotFound, e:
                res_data = {}
                res_data['status'] = 404
                res_data['errCode'] = -1
                res_data['errMsg'] = 'not found content'
                res_data['data'] = {}
                res.body = json.dumps(res_data)
            except Exception, e:
                res_data = {}
                res_data['status'] = 500
                res_data['errCode'] = -1
                res_data['errMsg'] = 'error'
                res_data['data'] = {}
                res.body = json.dumps(res_data)

        return response_service
