"""
Tests for the main FastAPI application.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """
    Test the root endpoint to ensure the application is running.
    """
    response = client.get("/test/")
    assert response.status_code == 200
    assert response.json() == {"message": "Application is running correctly"}


def test_submit_job():
    """
    Test the job submission endpoint.
    """
    response = client.post("/submit_job/", json={
        "input_image": "test_images/sample1.jp2",
        "output_image": "output/sample1_output.jp2",
        "operation": "decode"
    })
    assert response.status_code == 200
    assert response.json() == {"status": "Job submitted successfully"}


def test_submit_batch():
    """
    Test the batch job submission endpoint.
    """
    response = client.post("/submit_batch/", json={
        "jobs": [
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
    })
    assert response.status_code == 200
    assert response.json() == {"status": "Batch job submitted successfully"}
