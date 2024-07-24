"""
Tests for the tasks module.
"""

from app.tasks import decode_image, encode_image, create_slurm_script, submit_slurm_job
import os
import time
from unittest import mock

def test_decode_image():
    """
    Test the decode_image function.
    """
    input_image = "test_images/sample1.jp2"
    output_image = "output/sample1_output.jp2"
    gpu_id = 0

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_image), exist_ok=True)

    start_time = time.time()
    decode_image(input_image, output_image, gpu_id)
    end_time = time.time()
    duration = end_time - start_time
    assert os.path.exists(output_image)
    assert duration > 0  # Ensure it took some time to process

def test_encode_image():
    """
    Test the encode_image function.
    """
    input_image = "test_images/sample1.jp2"
    output_image = "output/sample1_encoded.jp2"
    gpu_id = 0

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_image), exist_ok=True)

    start_time = time.time()
    encode_image(input_image, output_image, gpu_id)
    end_time = time.time()
    duration = end_time - start_time
    assert os.path.exists(output_image)
    assert duration > 0  # Ensure it took some time to process

def test_create_slurm_script():
    """
    Test the create_slurm_script function.
    """
    input_image = "test_images/sample1.jp2"
    output_image = "output/sample1_output.jp2"
    operation = "decode"
    gpu_id = 0

    script_path = create_slurm_script(input_image, output_image, operation, gpu_id)
    assert os.path.exists(script_path)

def test_submit_slurm_job():
    """
    Test the submit_slurm_job function.
    """
    with mock.patch("subprocess.run", return_value=mock.Mock(stdout="Submitted batch job 12345\n")):
        script_path = "slurm_scripts/job_0.sh"
        priority = 0

        job_id = submit_slurm_job(script_path, priority)
        assert job_id == 12345
