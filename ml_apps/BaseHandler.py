import traceback
from time import time
from sanic import response
from sanic.log import logger, error_logger
from sanic.response import text
from sanic.views import HTTPMethodView



class BaseHandler(HTTPMethodView):

    def __init__(self, log_request=False):
        super().__init__()
        self.log_request=log_request

    async def get(self, request):
        return text('I am async get method')

    async def put(self, request):
        return text('I am async put method')

    async def post(self, request):
        data = request.json
        t1 = time()
        code = 1
        result = ""
        request_data=f"request: {data}, " if self.log_request else ""
        try:
            logger.info(f"requesting path: {request.path}... {request_data}")
            result = self.exec(data)
            message = 'success'
        except Exception as e:
            code = 0
            message = str(e)
            error_logger.error(f"request path: {request.path} error, {request_data} traceback: {e}\n{str(traceback.format_exc())}")
        t2 = time()
        res_dict = {"code": code, "msg": message, "data": result}
        logger.info(f"request path: {request.path} finished, exec cost: {t2 - t1:.3f}, {request_data} response: {res_dict}")
        return response.json(res_dict, ensure_ascii=False)

    def exec(self, json_inputs):
        raise NotImplementedError

    @classmethod
    def route_url(cls):
        raise NotImplementedError

    @classmethod
    def add_route(cls, app):
        app.add_route(cls.as_view(), cls.route_url())
