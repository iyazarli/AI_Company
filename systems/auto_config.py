"""
Otomatik AI Konfigüratörü
API key'lere göre optimal AI modellerini seçer
"""
from typing import Dict, Optional
from dataclasses import dataclass
import os


@dataclass
class AutoConfig:
    """Otomatik konfigürasyon"""
    mode: str  # 'demo', 'openai', 'anthropic', 'google', 'multi'
    available_providers: Dict[str, bool]
    assignments: Dict[str, Dict]
    role_overrides: Dict[str, str]


class AutoConfigurator:
    """API key'lere göre otomatik konfigürasyon"""
    
    def __init__(self):
        self.available_providers = self._detect_providers()
        self.optimal_config = self._create_optimal_config()
    
    def _detect_providers(self) -> Dict[str, bool]:
        """Hangi provider'lar kullanılabilir?"""
        return {
            'openai': bool(os.getenv('OPENAI_API_KEY')),
            'anthropic': bool(os.getenv('ANTHROPIC_API_KEY')),
            'google': bool(os.getenv('GOOGLE_API_KEY'))
        }
    
    def _create_optimal_config(self) -> AutoConfig:
        """Optimal konfigürasyonu oluştur"""
        providers = self.available_providers
        
        # Hiçbir API key yoksa demo mod
        if not any(providers.values()):
            return AutoConfig(
                mode='demo',
                available_providers=providers,
                assignments={
                    'enterprise': {'primary': 'demo/simulated', 'fallback': 'demo/simulated', 'tier': 'demo'},
                    'pro': {'primary': 'demo/simulated', 'fallback': 'demo/simulated', 'tier': 'demo'},
                    'basic': {'primary': 'demo/simulated', 'fallback': 'demo/simulated', 'tier': 'demo'}
                },
                role_overrides={}
            )
        
        # Assignments oluştur
        assignments = {}
        role_overrides = {}
        
        # Enterprise tier
        if providers['openai']:
            assignments['enterprise'] = {
                'primary': 'gpt-4-turbo',
                'fallback': 'claude-3-opus-20240229' if providers['anthropic'] else 'gpt-4',
                'tier': 'enterprise'
            }
            # Role overrides - kritik roller için GPT-4
            role_overrides = {
                'ceo': 'gpt-4-turbo',
                'cto': 'gpt-4-turbo',
                'architect': 'gpt-4-turbo'
            }
        elif providers['anthropic']:
            assignments['enterprise'] = {
                'primary': 'claude-3-opus-20240229',
                'fallback': 'claude-3-sonnet-20240229',
                'tier': 'enterprise'
            }
        
        # Pro tier
        if providers['openai']:
            assignments['pro'] = {
                'primary': 'gpt-4',
                'fallback': 'claude-3-sonnet-20240229' if providers['anthropic'] else 'gpt-3.5-turbo',
                'tier': 'pro'
            }
        elif providers['anthropic']:
            assignments['pro'] = {
                'primary': 'claude-3-sonnet-20240229',
                'fallback': 'claude-3-haiku-20240307',
                'tier': 'pro'
            }
        
        # Basic tier
        if providers['openai']:
            assignments['basic'] = {
                'primary': 'gpt-3.5-turbo',
                'fallback': 'claude-3-haiku-20240307' if providers['anthropic'] else 'gpt-3.5-turbo',
                'tier': 'basic'
            }
        elif providers['anthropic']:
            assignments['basic'] = {
                'primary': 'claude-3-haiku-20240307',
                'fallback': 'claude-3-haiku-20240307',
                'tier': 'basic'
            }
        elif providers['google']:
            assignments['basic'] = {
                'primary': 'gemini-pro',
                'fallback': 'gemini-pro',
                'tier': 'basic'
            }
        
        # Mode belirle
        if providers['openai'] and providers['anthropic']:
            mode = 'multi'
        elif providers['openai']:
            mode = 'openai'
        elif providers['anthropic']:
            mode = 'anthropic'
        elif providers['google']:
            mode = 'google'
        else:
            mode = 'demo'
        
        return AutoConfig(
            mode=mode,
            available_providers=providers,
            assignments=assignments,
            role_overrides=role_overrides
        )
    
    def get_model_for_role(self, difficulty_level: int, role_name: str = "") -> Dict:
        """Role zorluk seviyesine göre optimal model al"""
        config = self.optimal_config
        
        if config.mode == 'demo':
            return {
                'primary': 'demo/simulated',
                'fallback': 'demo/simulated',
                'tier': 'demo'
            }
        
        assignments = config.assignments
        
        # Role-specific override kontrolü
        if role_name and config.role_overrides:
            role_lower = role_name.lower()
            for key, model in config.role_overrides.items():
                if key in role_lower:
                    return {
                        'primary': model,
                        'fallback': assignments.get('pro', {}).get('fallback', model),
                        'tier': 'enterprise'
                    }
        
        # Zorluk seviyesine göre tier seç
        if difficulty_level >= 8:
            return assignments.get('enterprise', assignments.get('pro', assignments.get('basic')))
        elif difficulty_level >= 5:
            return assignments.get('pro', assignments.get('basic'))
        else:
            return assignments.get('basic', assignments.get('pro'))


# Singleton instance
_configurator = None

def get_auto_configurator() -> AutoConfigurator:
    """Singleton AutoConfigurator instance al"""
    global _configurator
    if _configurator is None:
        _configurator = AutoConfigurator()
    return _configurator
