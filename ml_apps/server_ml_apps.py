from sanic import Sanic
from BaseHandler import BaseHandler
from sanic.response import json, text
import base64
import os
import uuid
import time


app = Sanic("app-name")

class DoSomeHandler(BaseHandler):
    super().__init__(log_request=False)

    @classmethod
    def route_url(cls):
        return "/doSome"
    
    def exec(self, json_inputs):
        # res = model.run(json_input)
        res = 'some_res'
        return res


app.add_route(DoSomeHandler.as_view(), DoSomeHandler.route_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=4)