# About GPU Image Processor

## Overview

**GPU Image Processor** is a scalable API service designed for efficient processing of JPEG2000 images using GPU acceleration. This application leverages the power of NVIDIA GPUs and the nvJPEG2000 library to handle image encoding and decoding tasks. Built with FastAPI and Celery, it supports job prioritization, batch processing, and effective GPU resource management.

## Features

- **GPU Acceleration**: Utilizes NVIDIA GPUs for fast and efficient image processing.
- **API Service**: Provides RESTful endpoints for submitting image processing jobs.
- **Job Prioritization**: Supports prioritizing jobs based on urgency.
- **Batch Processing**: Capable of handling multiple jobs in a single batch to optimize GPU usage.
- **Resource Management**: Efficiently allocates and monitors GPU resources.
- **Scalable Architecture**: Built with microservices architecture for better scalability and maintainability.

## Technologies Used

- **FastAPI**: High-performance web framework for building APIs.
- **Celery**: Distributed task queue for managing background tasks.
- **Redis**: In-memory data structure store used as a message broker for Celery.
- **nvJPEG2000**: NVIDIA library for accelerated JPEG2000 image decoding and encoding.
- **Docker**: Containerization for consistent development and deployment environments.
- **Python**: Programming language used for the core application logic.

## Getting Started

### Prerequisites

- **Docker**: Ensure Docker is installed on your system. You can download it from [docker.com](https://www.docker.com/products/docker-desktop).
- **Python**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/gpu-image-processor.git
   cd gpu-image-processor
   ```

2. **Set Up Docker Compose**:
   Ensure you have the `docker-compose.yml` file set up as described:
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "8000:8000"
       depends_on:
         - redis

     worker:
       build: .
       command: celery -A app.tasks worker --loglevel=info
       depends_on:
         - redis

     beat:
       build: .
       command: celery -A app.tasks beat --loglevel=info
       depends_on:
         - redis

     redis:
       image: "redis:alpine"
   ```

3. **Build and Start the Services**:
   ```bash
   docker-compose up --build
   ```

4. **Access the API**:
   - Open your browser and go to `http://localhost:8000`.

### Usage

- **Submit an Individual Job**:
  Use the `/submit_job/` endpoint to submit a single image processing job.
  ```json
  POST /submit_job/
  {
    "input_image": "path/to/input_image.jp2",
    "output_image": "path/to/output_image.jp2",
    "operation": "decode",  // or "encode"
    "priority": 1
  }
  ```

- **Submit a Batch Job**:
  Use the `/submit_batch/` endpoint to submit a batch of image processing jobs.
  ```json
  POST /submit_batch/
  {
    "jobs": [
      {
        "input_image": "path/to/input_image1.jp2",
        "output_image": "path/to/output_image1.jp2",
        "operation": "decode"
      },
      {
        "input_image": "path/to/input_image2.jp2",
        "output_image": "path/to/output_image2.jp2",
        "operation": "encode"
      }
    ]
  }
  ```

### Development

1. **Set Up the Development Environment**:
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

2. **Run the FastAPI Server Locally**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. **Run Celery Worker and Beat Locally**:
   ```bash
   celery -A app.tasks worker --loglevel=info
   celery -A app.tasks beat --loglevel=info
   ```

### Contributing

We welcome contributions from the community! To contribute, please follow these steps:

1. **Fork the Repository**: Click on the "Fork" button at the top right of this page.
2. **Clone Your Fork**: Clone your forked repository to your local machine.
   ```bash
   git clone https://github.com/your-username/gpu-image-processor.git
   ```
3. **Create a Branch**: Create a new branch for your feature or bugfix.
   ```bash
   git checkout -b feature-name
   ```
4. **Commit Your Changes**: Make your changes and commit them with a clear message.
   ```bash
   git commit -m "Add feature-name"
   ```
5. **Push to Your Fork**: Push your changes to your forked repository.
   ```bash
   git push origin feature-name
   ```
6. **Create a Pull Request**: Go to the original repository and create a pull request from your fork.

---
### Contact

If you have any questions or feedback, please feel free to reach out.

---
