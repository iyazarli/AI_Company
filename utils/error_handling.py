"""
Exception Handling Utilities
"""
import functools
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def handle_errors(default_return=None, log_errors=True):
    """
    Decorator for graceful error handling
    
    Usage:
        @handle_errors(default_return={}, log_errors=True)
        def risky_function():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                return default_return
        return wrapper
    return decorator

def safe_get(obj, *keys, default=None):
    """
    Safely get nested dictionary/object values
    
    Usage:
        value = safe_get(data, 'user', 'profile', 'name', default='Unknown')
    """
    for key in keys:
        try:
            if isinstance(obj, dict):
                obj = obj.get(key)
            else:
                obj = getattr(obj, key, None)
            
            if obj is None:
                return default
        except (KeyError, AttributeError, TypeError):
            return default
    
    return obj if obj is not None else default
