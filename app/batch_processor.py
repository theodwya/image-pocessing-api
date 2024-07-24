"""
Batch Processor Module

This module handles the batch processing of image jobs using the nvJPEG2000 library.
Jobs are processed in batches to optimize GPU usage.
"""

from celery import Celery
from .gpu_manager import gpu_manager
import os

# Conditionally import the actual or mock nvJPEG2000 library based on the
# environment variable
if os.getenv("USE_MOCK_NVJPEG2000", "true").lower() == "true":
    from .mock_nvjpeg2000 import *
else:
    import nvjpeg2000

# Create a Celery instance for batch processing
celery = Celery(
    'batch_processor',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0')


@celery.task
def process_batch(jobs):
    """
    Process a batch of image jobs.

    Args:
        jobs (list): A list of job dictionaries, each containing 'input_image', 'output_image', and 'operation'.

    Returns:
        list: A list of results for each job.
    """
    gpu_id = gpu_manager.allocate_gpu()
    if gpu_id is None:
        return "No GPU available. Please try again later."

    try:
        results = []
        for job in jobs:
            input_image, output_image, operation = job['input_image'], job['output_image'], job['operation']
            if operation == 'decode':
                decode_image(input_image, output_image, gpu_id)
            elif operation == 'encode':
                encode_image(input_image, output_image, gpu_id)
            results.append(f"Job {input_image} completed successfully")
        return results
    except Exception as e:
        return str(e)
    finally:
        gpu_manager.release_gpu(gpu_id)


def decode_image(input_image, output_image, gpu_id):
    """
    Decode a JPEG2000 image using the specified GPU.

    Args:
        input_image (str): Path to the input image file.
        output_image (str): Path to the output image file.
        gpu_id (int): The ID of the GPU to use.
    """
    nvjpeg2k_handle = nvjpeg2kCreate()
    nvjpeg2k_decode_state = nvjpeg2kDecodeStateCreate(nvjpeg2k_handle)
    nvjpeg2k_stream = nvjpeg2kStreamCreate(nvjpeg2k_handle)

    with open(input_image, 'rb') as f:
        image_data = f.read()

    nvjpeg2kStreamParse(
        nvjpeg2k_handle,
        nvjpeg2k_stream,
        image_data,
        len(image_data))

    image_info = nvjpeg2kStreamGetImageInfo(nvjpeg2k_stream)
    width, height, num_components = image_info.width, image_info.height, image_info.num_components
    decoded_image = nvjpeg2kDecode(
        nvjpeg2k_handle,
        nvjpeg2k_decode_state,
        nvjpeg2k_stream,
        width,
        height,
        num_components,
        gpu_id)

    with open(output_image, 'wb') as f:
        f.write(decoded_image)

    nvjpeg2kDecodeStateDestroy(nvjpeg2k_decode_state)
    nvjpeg2kStreamDestroy(nvjpeg2k_stream)
    nvjpeg2kDestroy(nvjpeg2k_handle)


def encode_image(input_image, output_image, gpu_id):
    """
    Encode an image to JPEG2000 format using the specified GPU.

    Args:
        input_image (str): Path to the input image file.
        output_image (str): Path to the output image file.
        gpu_id (int): The ID of the GPU to use.
    """
    nvjpeg2k_handle = nvjpeg2kCreate()
    nvjpeg2k_encode_state = nvjpeg2kEncodeStateCreate(nvjpeg2k_handle)
    nvjpeg2k_stream = nvjpeg2kStreamCreate(nvjpeg2k_handle)

    with open(input_image, 'rb') as f:
        image_data = f.read()

    nvjpeg2kStreamParse(
        nvjpeg2k_handle,
        nvjpeg2k_stream,
        image_data,
        len(image_data))

    encoded_image = nvjpeg2kEncode(
        nvjpeg2k_handle,
        nvjpeg2k_encode_state,
        nvjpeg2k_stream,
        gpu_id)

    with open(output_image, 'wb') as f:
        f.write(encoded_image)

    nvjpeg2kEncodeStateDestroy(nvjpeg2k_encode_state)
    nvjpeg2kStreamDestroy(nvjpeg2k_stream)
    nvjpeg2kDestroy(nvjpeg2k_handle)
