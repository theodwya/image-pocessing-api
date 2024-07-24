"""
Tests for the tasks module.
"""

from app.tasks import decode_image, encode_image, create_slurm_script, submit_slurm_job
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

def test_submit_slurm_job(mocker):
    """
    Test the submit_slurm_job function.
    """
    mocker.patch("subprocess.run", return_value=mocker.Mock(stdout="Submitted batch job 12345\n"))
    script_path = "slurm_scripts/job_0.sh"
    priority = 0

    job_id = submit_slurm_job(script_path, priority)
    assert job_id == 12345
