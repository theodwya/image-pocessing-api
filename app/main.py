"""
Main module for FastAPI application.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from .tasks import process_image
import shutil
import os
import uuid

app = FastAPI()

# Ensure the upload and output directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), operation: str = "decode"):
    """
    Endpoint to upload an image file and process it.

    Args:
        file (UploadFile): The uploaded image file.
        operation (str): The operation to perform ('decode' or 'encode').

    Returns:
        dict: Status message and file information.
    """
    if operation not in ["decode", "encode"]:
        raise HTTPException(status_code=400, detail="Invalid operation")

    file_id = str(uuid.uuid4())
    input_image_path = f"uploads/{file_id}_{file.filename}"
    output_image_path = f"output/{file_id}_{file.filename}"

    # Save the uploaded file
    with open(input_image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Submit the image processing job
    result = process_image.apply_async(
        (input_image_path, output_image_path, operation))

    return {"status": "File uploaded successfully", "task_id": result.id, "file_id": file_id}


@app.get("/images/{file_id}")
async def get_image(file_id: str):
    """
    Endpoint to retrieve an image file.

    Args:
        file_id (str): The ID of the file to retrieve.

    Returns:
        FileResponse: The requested image file.
    """
    file_path = f"output/{file_id}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


@app.put("/images/{file_id}")
async def update_image(file_id: str, file: UploadFile = File(...)):
    """
    Endpoint to update an existing image file.

    Args:
        file_id (str): The ID of the file to update.
        file (UploadFile): The new image file.

    Returns:
        dict: Status message.
    """
    input_image_path = f"uploads/{file_id}"
    output_image_path = f"output/{file_id}"

    # Save the new file
    with open(input_image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Submit the image processing job
    result = process_image.apply_async(
        (input_image_path, output_image_path, "decode"))

    return {"status": "File updated successfully", "task_id": result.id}


@app.delete("/images/{file_id}")
async def delete_image(file_id: str):
    """
    Endpoint to delete an image file.

    Args:
        file_id (str): The ID of the file to delete.

    Returns:
        dict: Status message.
    """
    input_image_path = f"uploads/{file_id}"
    output_image_path = f"output/{file_id}"

    if os.path.exists(input_image_path):
        os.remove(input_image_path)
    if os.path.exists(output_image_path):
        os.remove(output_image_path)

    return {"status": "File deleted successfully"}
