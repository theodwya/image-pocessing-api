"""
GPU Manager Module

This module manages the allocation and deallocation of GPU resources.
It also monitors the GPU usage continuously to ensure efficient utilization.
"""

import threading
from time import sleep
import psutil

class GPUManager:
    """
    A class to manage GPU resources.

    Attributes:
        num_gpus (int): The total number of GPUs available.
        lock (threading.Lock): A lock to manage concurrent access to GPUs.
        available_gpus (list): A list of available GPU IDs.
        gpu_usage (list): A list to store the usage of each GPU.
    """
    def __init__(self, num_gpus):
        """
        Initialize the GPUManager with the number of GPUs.
        
        Args:
            num_gpus (int): The total number of GPUs.
        """
        self.num_gpus = num_gpus
        self.lock = threading.Lock()
        self.available_gpus = list(range(num_gpus))
        self.gpu_usage = [0] * num_gpus  # Track GPU usage

    def allocate_gpu(self):
        """
        Allocate a GPU for a task.
        
        Returns:
            int: The ID of the allocated GPU, or None if no GPU is available.
        """
        with self.lock:
            if self.available_gpus:
                return self.available_gpus.pop(0)
            return None

    def release_gpu(self, gpu_id):
        """
        Release a GPU after a task is done.
        
        Args:
            gpu_id (int): The ID of the GPU to release.
        """
        with self.lock:
            self.available_gpus.append(gpu_id)

    def monitor_gpu_usage(self):
        """
        Continuously monitor the usage of each GPU.
        """
        while True:
            for gpu_id in range(self.num_gpus):
                # Simulated GPU usage monitoring
                self.gpu_usage[gpu_id] = psutil.cpu_percent(interval=1)
            sleep(5)  # Monitor every 5 seconds

# Create a singleton GPUManager instance
gpu_manager = GPUManager(num_gpus=4)

# Start GPU usage monitoring in a separate thread
threading.Thread(target=gpu_manager.monitor_gpu_usage, daemon=True).start()
