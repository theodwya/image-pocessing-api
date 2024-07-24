"""
Tasks Module

This module defines the Celery tasks for processing image jobs using the nvJPEG2000 library.
"""

from celery import Celery
from .gpu_manager import gpu_manager
import os

# Conditionally import the actual or mock nvJPEG2000 library based on the environment variable
if os.getenv("USE_MOCK_NVJPEG2000", "true").lower() == "true":
    from .mock_nvjpeg2000 import *
else:
    import nvjpeg2000

# Create a Celery instance for task management
celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@celery.task
def process_image(input_image, output_image, operation, priority=0):
    """
    Process an individual image job.

    Args:
        input_image (str): Path to the input image file.
        output_image (str): Path to the output image file.
        operation (str): Operation to perform ('decode' or 'encode').
        priority (int): Priority of the job (default is 0).
    
    Returns:
        str: Status message.
    """
    gpu_id = gpu_manager.allocate_gpu()
    if gpu_id is None:
        return "No GPU available. Please try again later."

    try:
        if operation == 'decode':
            decode_image(input_image, output_image, gpu_id)
        elif operation == 'encode':
            encode_image(input_image, output_image, gpu_id)
        return "Job completed successfully"
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

    nvjpeg2kStreamParse(nvjpeg2k_handle, nvjpeg2k_stream, image_data, len(image_data))

    image_info = nvjpeg2kStreamGetImageInfo(nvjpeg2k_stream)
    width, height, num_components = image_info.width, image_info.height, image_info.num_components
    decoded_image = nvjpeg2kDecode(nvjpeg2k_handle, nvjpeg2k_decode_state, nvjpeg2k_stream, width, height, num_components, gpu_id)

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

    nvjpeg2kStreamParse(nvjpeg2k_handle, nvjpeg2k_stream, image_data, len(image_data))

    encoded_image = nvjpeg2kEncode(nvjpeg2k_handle, nvjpeg2k_encode_state, nvjpeg2k_stream, gpu_id)

    with open(output_image, 'wb') as f:
        f.write(encoded_image)

    nvjpeg2kEncodeStateDestroy(nvjpeg2k_encode_state)
    nvjpeg2kStreamDestroy(nvjpeg2k_stream)
    nvjpeg2kDestroy(nvjpeg2k_handle)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Setup periodic tasks for Celery.

    Args:
        sender (celery.app.base.Celery): The Celery app instance.
        kwargs (dict): Additional arguments.
    """
    sender.add_periodic_task(crontab(minute='*/1'), check_gpu_status.s())

@celery.task
def check_gpu_status():
    """
    Periodic task to check the status of GPU usage.
    """
    gpu_usage = gpu_manager.gpu_usage
    print(f"GPU Usage: {gpu_usage}")