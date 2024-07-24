"""
Tests for the batch_processor module.
"""

from app.batch_processor import process_batch
import os

def test_process_batch():
    """
    Test the process_batch function.
    """
    jobs = [
        {
            "input_image": "test_images/sample1.jp2",
            "output_image": "output/sample1_output.jp2",
            "operation": "decode"
        },
        {
            "input_image": "test_images/sample2.jp2",
            "output_image": "output/sample2_output.jp2",
            "operation": "decode"
        }
    ]

    # Ensure the output directory exists
    for job in jobs:
        os.makedirs(os.path.dirname(job['output_image']), exist_ok=True)

    results = process_batch(jobs)
    assert all(os.path.exists(job['output_image']) for job in jobs)
