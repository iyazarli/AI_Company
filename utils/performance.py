"""
Performance Monitoring Utilities
"""
import time
import functools
import logging
from typing import Callable

logger = logging.getLogger(__name__)

def timer(func: Callable) -> Callable:
    """
    Function execution time decorator
    
    Usage:
        @timer
        def slow_function():
            time.sleep(1)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
        
        return result
    return wrapper

class PerformanceMonitor:
    """Context manager for performance monitoring"""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        logger.info(f"Starting: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.time() - self.start_time
        
        if exc_type:
            logger.error(
                f"{self.operation_name} failed after {execution_time:.4f}s: {exc_val}"
            )
        else:
            logger.info(
                f"{self.operation_name} completed in {execution_time:.4f}s"
            )
        
        return False  # Don't suppress exceptions

# Usage:
# with PerformanceMonitor("API Call"):
#     response = api.call()
