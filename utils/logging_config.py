"""
Logging Configuration - Merkezi logging sistemi
"""
import logging
import sys
from pathlib import Path

def setup_logging(log_level=logging.INFO, log_file=None):
    """
    Merkezi logging yapılandırması
    
    Args:
        log_level: Logging seviyesi (DEBUG, INFO, WARNING, ERROR)
        log_file: Log dosyası yolu (opsiyonel)
    """
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # File handler (opsiyonel)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger

# Modül başına logger oluşturma helper
def get_logger(name):
    """Modül için logger oluştur"""
    return logging.getLogger(name)
