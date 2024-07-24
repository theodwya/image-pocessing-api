"""
Tests for the tasks module.
"""

from app.tasks import decode_image, encode_image
import os

def test_decode_image():
    """
    Test the decode_image function.
    """
    input_image = "test_images/sample1.jp2"
    output_image = "output/sample1_output.jp2"
    gpu_id = 0

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_image), exist_ok=True)

    decode_image(input_image, output_image, gpu_id)
    assert os.path.exists(output_image)

def test_encode_image():
    """
    Test the encode_image function.
    """
    input_image = "test_images/sample1.jp2"
    output_image = "output/sample1_encoded.jp2"
    gpu_id = 0

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_image), exist_ok=True)

    encode_image(input_image, output_image, gpu_id)
    assert os.path.exists(output_image)
