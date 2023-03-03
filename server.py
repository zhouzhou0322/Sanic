from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json, text
import base64
import os
import uuid
import time


app = Sanic(__name__)

class MyView(HTTPMethodView):
    async def get(self, request):
        return json({'method': 'GET'})
    
    async def post(self, request):
        return json({'method': 'POST'})

class UploadView(HTTPMethodView):
    async def post(self, request):
        start_time = time.perf_counter()
        if 'image' not in request.json:
            return text('Missing image data.', status=400)
        image_data = base64.b64decode(request.json['image'])
        filename = str("a") + '.jpg'
        file_path = os.path.join('../img/', filename)
        with open(file_path, 'wb') as f:
            f.write(image_data)
            
        end_time = time.perf_counter()
        duration = end_time - start_time
        #print(f"Execution time: {duration:.6f} seconds")
        return json({'status': 'success', 'filename': filename})

app.add_route(MyView.as_view(), '/')
app.add_route(UploadView.as_view(), '/upload')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=4)