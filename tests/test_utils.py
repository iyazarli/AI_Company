"""
Unit Tests - Utils Tests
"""
import unittest
import logging
import os
from pathlib import Path
from utils.logging_config import setup_logging, get_logger
from utils.error_handling import handle_errors, safe_get
# Config helper test edilebilmesi için yaml gerekiyor, hata varsa skip et
try:
    from utils.config_helper import Config
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

logger = logging.getLogger(__name__)

class TestLoggingConfig(unittest.TestCase):
    """Logging configuration tests"""
    
    def test_get_logger(self):
        """Test logger creation"""
        test_logger = get_logger("test_module")
        self.assertIsInstance(test_logger, logging.Logger)
        self.assertEqual(test_logger.name, "test_module")

class TestErrorHandling(unittest.TestCase):
    """Error handling tests"""
    
    def test_safe_get_dict(self):
        """Test safe dictionary access"""
        data = {'user': {'profile': {'name': 'John'}}}
        
        result = safe_get(data, 'user', 'profile', 'name')
        self.assertEqual(result, 'John')
        
        result = safe_get(data, 'user', 'invalid', default='Unknown')
        self.assertEqual(result, 'Unknown')
    
    def test_safe_get_object(self):
        """Test safe object access"""
        class User:
            def __init__(self):
                self.name = "Alice"
        
        user = User()
        result = safe_get(user, 'name')
        self.assertEqual(result, 'Alice')
        
        result = safe_get(user, 'age', default=0)
        self.assertEqual(result, 0)
    
    def test_handle_errors_decorator(self):
        """Test error handling decorator"""
        @handle_errors(default_return=0, log_errors=False)
        def risky_function():
            return 1 / 0
        
        result = risky_function()
        self.assertEqual(result, 0)
    
    def test_handle_errors_success(self):
        """Test error handling with successful function"""
        @handle_errors(default_return=0, log_errors=False)
        def safe_function():
            return 42
        
        result = safe_function()
        self.assertEqual(result, 42)

class TestConfigHelper(unittest.TestCase):
    """Config helper tests"""
    
    @unittest.skipUnless(YAML_AVAILABLE, "yaml module not available")
    def test_get_project_root(self):
        """Test project root detection"""
        root = Config.get_project_root()
        self.assertIsInstance(root, Path)
        self.assertTrue(root.exists())
    
    @unittest.skipUnless(YAML_AVAILABLE, "yaml module not available")
    def test_get_config_path(self):
        """Test config path generation"""
        config_path = Config.get_config_path('test.yaml')
        self.assertIsInstance(config_path, Path)
        self.assertTrue(str(config_path).endswith('config/test.yaml'))
    
    @unittest.skipUnless(YAML_AVAILABLE, "yaml module not available")
    def test_get_env(self):
        """Test environment variable retrieval"""
        os.environ['TEST_VAR'] = 'test_value'
        
        result = Config.get_env('TEST_VAR')
        self.assertEqual(result, 'test_value')
        
        result = Config.get_env('NONEXISTENT', default='default')
        self.assertEqual(result, 'default')
        
        del os.environ['TEST_VAR']

if __name__ == '__main__':
    unittest.main()
