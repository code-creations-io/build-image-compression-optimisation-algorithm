import os
import uuid
import logging

from algorithm.optimisation import Optimiser

logger = logging.getLogger()
logger.setLevel(logging.INFO)

IMAGE_FILE = "image.png"

if __name__ == "__main__":

    # Load image as bytes
    with open(IMAGE_FILE, 'rb') as f:
        img_bytes = f.read()

    original_size = len(img_bytes)
    print(f"Original image size: {original_size} bytes")

    # Optimise image with compression
    extension = IMAGE_FILE.split('.')[-1]
    optimiser = Optimiser()
    optimised_img = optimiser.optimise(
        bytes_array=img_bytes,
        filename=f"{uuid.uuid4()}.{extension}"
    )

    output_path = os.path.join(os.getcwd(), 'image_compressed.png')
    with open(output_path, 'wb') as f:
        f.write(optimised_img)

    compressed_size = os.path.getsize(output_path)
