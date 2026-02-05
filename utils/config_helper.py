"""
Configuration Utilities - Path ve config yönetimi
"""
import os
from pathlib import Path
import yaml
from typing import Dict, Any

class Config:
    """Merkezi konfigürasyon yöneticisi"""
    
    @staticmethod
    def get_project_root() -> Path:
        """Proje root dizinini döndür"""
        # Bu dosyanın konumundan root'u bul
        return Path(__file__).parent.parent
    
    @staticmethod
    def get_config_path(filename: str) -> Path:
        """Config dosyası yolunu döndür"""
        return Config.get_project_root() / 'config' / filename
    
    @staticmethod
    def load_yaml(filepath: str | Path) -> Dict[str, Any]:
        """YAML dosyasını yükle"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")
        
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def get_env(key: str, default: str = None) -> str:
        """Environment variable'ı al"""
        return os.getenv(key, default)
    
    @staticmethod
    def is_production() -> bool:
        """Production ortamında mı?"""
        return os.getenv('ENVIRONMENT', 'development') == 'production'
    
    @staticmethod
    def is_streamlit_cloud() -> bool:
        """Streamlit Cloud'da mı?"""
        return os.getenv('STREAMLIT_SHARING_MODE') == 'true' or \
               os.path.exists('/mount/src')
