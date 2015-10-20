import logging
import uuid

__author__ = 'jiyue'


class TracerMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger("main.tracer")

    def trace_request(self, req):
        context = []
        for k, v in req.params.iteritems():
            context.append(v)

        for k, v in req.headers.iteritems():
            context.append(v)

        self.logger.info('|'.join(context));

    def process_request(self, req, resp):
        self.logger.info(req.params)
        req.params['rid'] = str(uuid.uuid1())
        self.trace_request(req)


class AuthenticateMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger("main.authenticate")

    def process_request(self, req, resp):
        self.logger.info("remote addr:%s", req)
        self.authenticate(req)

    def authenticate(self, request):
        pass
