"""
AI Provider Yöneticisi
Farklı AI provider'larını (OpenAI, Anthropic, Google) yönetir
"""
from typing import Dict, Optional, List
from enum import Enum
from dataclasses import dataclass
import os


class AITier(str, Enum):
    """AI Model seviyeleri"""
    ENTERPRISE = "enterprise"
    PRO = "pro"
    BASIC = "basic"
    DEMO = "demo"


@dataclass
class AIModel:
    """AI Model bilgisi"""
    provider: str
    model_name: str
    tier: AITier
    cost: float
    strengths: List[str]
    best_for: List[str]
    context_window: int


@dataclass
class RoleAIAssignment:
    """Role için AI ataması"""
    role: str
    primary_ai: str
    fallback_ai: str
    tier: AITier
    difficulty_level: int
    reasoning: str


class AIProvider:
    """AI Provider yöneticisi"""
    
    def __init__(self, auto_mode: bool = True):
        self.auto_mode = auto_mode
        self.auto_config = None
        
        if auto_mode:
            from systems.auto_config import get_auto_configurator
            self.auto_config = get_auto_configurator()
        
        self.providers = self._load_provider_config()
        self.api_keys = self._load_api_keys()
    
    def _load_provider_config(self) -> Dict:
        """Provider konfigürasyonları"""
        return {
            'openai': {
                'name': 'OpenAI',
                'models': {
                    'gpt-4-turbo': {
                        'tier': 'enterprise',
                        'cost': 0.01,
                        'strengths': ['reasoning', 'coding', 'analysis'],
                        'best_for': ['complex tasks', 'critical decisions'],
                        'context_window': 128000
                    },
                    'gpt-4': {
                        'tier': 'pro',
                        'cost': 0.03,
                        'strengths': ['reasoning', 'coding'],
                        'best_for': ['important tasks'],
                        'context_window': 8192
                    },
                    'gpt-3.5-turbo': {
                        'tier': 'basic',
                        'cost': 0.002,
                        'strengths': ['speed', 'efficiency'],
                        'best_for': ['simple tasks'],
                        'context_window': 16384
                    }
                }
            },
            'anthropic': {
                'name': 'Anthropic',
                'models': {
                    'claude-3-opus-20240229': {
                        'tier': 'enterprise',
                        'cost': 0.015,
                        'strengths': ['reasoning', 'analysis', 'writing'],
                        'best_for': ['complex analysis', 'critical thinking'],
                        'context_window': 200000
                    },
                    'claude-3-sonnet-20240229': {
                        'tier': 'pro',
                        'cost': 0.003,
                        'strengths': ['balanced', 'efficient'],
                        'best_for': ['general tasks'],
                        'context_window': 200000
                    },
                    'claude-3-haiku-20240307': {
                        'tier': 'basic',
                        'cost': 0.00025,
                        'strengths': ['speed', 'cost-effective'],
                        'best_for': ['simple tasks'],
                        'context_window': 200000
                    }
                }
            },
            'google': {
                'name': 'Google',
                'models': {
                    'gemini-pro': {
                        'tier': 'basic',
                        'cost': 0.00025,
                        'strengths': ['multimodal', 'speed'],
                        'best_for': ['general tasks'],
                        'context_window': 32768
                    }
                }
            },
            'demo': {
                'name': 'Demo Mode',
                'models': {
                    'simulated': {
                        'tier': 'demo',
                        'cost': 0.0,
                        'strengths': ['testing'],
                        'best_for': ['testing without API keys'],
                        'context_window': 4096
                    }
                }
            }
        }
    
    def _load_api_keys(self) -> Dict[str, str]:
        """API anahtarlarını yükle"""
        return {
            'openai': os.getenv('OPENAI_API_KEY', ''),
            'anthropic': os.getenv('ANTHROPIC_API_KEY', ''),
            'google': os.getenv('GOOGLE_API_KEY', '')
        }
    
    def assign_ai_to_role(self, role: str, difficulty: int) -> RoleAIAssignment:
        """Role için AI ata"""
        
        # Otomatik mod aktifse
        if self.auto_mode and self.auto_config:
            model_config = self.auto_config.get_model_for_role(difficulty, role)
            return RoleAIAssignment(
                role=role,
                primary_ai=model_config['primary'],
                fallback_ai=model_config['fallback'],
                tier=AITier(model_config['tier']),
                difficulty_level=difficulty,
                reasoning="Auto-configured"
            )
        
        # Manuel mod - varsayılan atama
        return RoleAIAssignment(
            role=role,
            primary_ai="demo/simulated",
            fallback_ai="demo/simulated",
            tier=AITier.DEMO,
            difficulty_level=difficulty,
            reasoning="Demo mode - add API keys for real AI"
        )
    
    def get_model_info(self, model_path: str) -> Optional[AIModel]:
        """Model bilgisini al (örn: 'openai/gpt-4')"""
        try:
            if '/' in model_path:
                provider, model_name = model_path.split('/')
            else:
                # Sadece model ismi verilmişse demo olarak kabul et
                provider = 'demo'
                model_name = model_path
            
            if provider in self.providers:
                models = self.providers[provider].get('models', {})
                if model_name in models:
                    model_config = models[model_name]
                    return AIModel(
                        provider=provider,
                        model_name=model_name,
                        tier=AITier(model_config['tier']),
                        cost=model_config['cost'],
                        strengths=model_config['strengths'],
                        best_for=model_config['best_for'],
                        context_window=model_config['context_window']
                    )
            
            # Bulunamadıysa None
            return None
            
        except Exception:
            return None
    
    def create_client(self, model_path: str):
        """AI client oluştur"""
        try:
            provider = model_path.split('/')[0] if '/' in model_path else 'demo'
            
            # Demo mode
            if provider == 'demo' or not self.api_keys.get(provider):
                return self._create_demo_client()
            
            # OpenAI
            if provider == 'openai' and self.api_keys['openai']:
                from langchain_openai import ChatOpenAI
                model_name = model_path.split('/')[1]
                return ChatOpenAI(
                    model=model_name,
                    api_key=self.api_keys['openai']
                )
            
            # Anthropic
            if provider == 'anthropic' and self.api_keys['anthropic']:
                from langchain_anthropic import ChatAnthropic
                model_name = model_path.split('/')[1]
                return ChatAnthropic(
                    model=model_name,
                    api_key=self.api_keys['anthropic']
                )
            
            # Google
            if provider == 'google' and self.api_keys['google']:
                from langchain_google_genai import ChatGoogleGenerativeAI
                model_name = model_path.split('/')[1]
                return ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=self.api_keys['google']
                )
            
            # Fallback to demo
            return self._create_demo_client()
            
        except Exception:
            return self._create_demo_client()
    
    def _create_demo_client(self):
        """Demo client - API key olmadan"""
        from langchain.schema import AIMessage
        
        class DemoLLM:
            async def ainvoke(self, messages):
                return AIMessage(content="[Demo Mode] Bu bir simülasyon yanıtıdır. Gerçek AI yanıtı için API key ekleyin.")
        
        return DemoLLM()


# Singleton instance
_provider = None

def get_ai_provider(auto_mode: bool = True) -> AIProvider:
    """Singleton AIProvider instance al"""
    global _provider
    if _provider is None:
        _provider = AIProvider(auto_mode=auto_mode)
    return _provider
