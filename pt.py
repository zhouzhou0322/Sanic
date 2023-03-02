# pressure test
import base64
import io
import requests
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import uuid
import os
from tqdm import tqdm


def send_image(image_data):

    # Send the image to the Sanic server
    response = requests.post('http://localhost:8000/upload', json={'image': image_data})

    return response


def main(num_requests):
    # Generate a white image with Pillow
    image = Image.new('RGB', (300, 300), color='white')

    # Encode the image as base64
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Send the image to the Sanic server in parallel
    with ThreadPoolExecutor(max_workers=1000) as executor:
        future_responses = [executor.submit(send_image, base64_image) for i in range(num_requests)]

    # Wait for all responses to complete
    responses = [f.result() for f in future_responses]

    # Print the average response time and QPS
    total_time = sum(r.elapsed.seconds + r.elapsed.microseconds / 1000000 for r in responses)

    avg_time = total_time / num_requests
    qps = num_requests / total_time
    print(f"Avg. response time: {avg_time:.3f} s")
    print(f"QPS: {qps:.1f}")


if __name__ == '__main__':
    main(1000)