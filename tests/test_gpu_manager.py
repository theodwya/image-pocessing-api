"""
Tests for the GPUManager class.
"""

from app.gpu_manager import gpu_manager

def test_allocate_gpu():
    """
    Test GPU allocation.
    """
    gpu_id = gpu_manager.allocate_gpu()
    assert gpu_id is not None
    assert gpu_id in range(gpu_manager.num_gpus)

def test_release_gpu():
    """
    Test GPU release.
    """
    gpu_id = gpu_manager.allocate_gpu()
    gpu_manager.release_gpu(gpu_id)
    assert gpu_id in gpu_manager.available_gpus
