"""
Main Application Module

This module sets up the FastAPI application and defines the API endpoints for job submission.
"""

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from .tasks import process_image
from .batch_processor import process_batch

# Create a FastAPI application instance
app = FastAPI()


class JobRequest(BaseModel):
    """
    Model for an individual job request.

    Attributes:
        input_image (str): Path to the input image file.
        output_image (str): Path to the output image file.
        operation (str): Operation to perform ('decode' or 'encode').
        priority (int): Priority of the job (default is 0).
    """
    input_image: str
    output_image: str
    operation: str  # 'decode' or 'encode'
    priority: int = 0  # Job priority


class BatchJobRequest(BaseModel):
    """
    Model for a batch job request.

    Attributes:
        jobs (list): A list of JobRequest objects.
    """
    jobs: list[JobRequest]


@app.post("/submit_job/")
async def submit_job(job: JobRequest, background_tasks: BackgroundTasks):
    """
    Endpoint to submit an individual job.

    Args:
        job (JobRequest): The job request data.
        background_tasks (BackgroundTasks): Background tasks instance for running tasks asynchronously.

    Returns:
        dict: Status message.
    """
    background_tasks.add_task(
        process_image,
        job.input_image,
        job.output_image,
        job.operation,
        job.priority)
    return {"status": "Job submitted successfully"}


@app.post("/submit_batch/")
async def submit_batch(
        batch_job: BatchJobRequest,
        background_tasks: BackgroundTasks):
    """
    Endpoint to submit a batch of jobs.

    Args:
        batch_job (BatchJobRequest): The batch job request data.
        background_tasks (BackgroundTasks): Background tasks instance for running tasks asynchronously.

    Returns:
        dict: Status message.
    """
    jobs = [{"input_image": job.input_image,
             "output_image": job.output_image,
             "operation": job.operation} for job in batch_job.jobs]
    background_tasks.add_task(process_batch, jobs)
    return {"status": "Batch job submitted successfully"}


@app.get("/test/")
async def read_root():
    """
    A test endpoint to verify that the application is running correctly.

    Returns:
        dict: A simple message indicating the application is running.
    """
    return {"message": "Application is running correctly"}
