import base64
import io
import requests
from PIL import Image

# Generate a white image with Pillow
image = Image.new('RGB', (300, 300), color='white')

# Encode the image as base64
buffer = io.BytesIO()
image.save(buffer, format='JPEG')
base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

# Send the image to the Sanic server
response = requests.post('http://localhost:8000/upload', json={'image': base64_image})

print(response.json())
