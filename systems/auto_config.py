"""
Auto AI Configuration - API key'lere göre otomatik AI ataması
"""
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class AutoAIConfigurator:
    """API key'lere göre otomatik AI konfigürasyonu"""
    
    def __init__(self):
        self.available_providers = self._detect_available_providers()
        self.optimal_config = self._generate_optimal_config()
    
    def _detect_available_providers(self) -> Dict[str, bool]:
        """Hangi AI provider'ların API key'i var?"""
        providers = {
            'openai': bool(os.getenv('OPENAI_API_KEY')),
            'anthropic': bool(os.getenv('ANTHROPIC_API_KEY')),
            'google': bool(os.getenv('GOOGLE_API_KEY')),
            'mistral': bool(os.getenv('MISTRAL_API_KEY')),
            'cohere': bool(os.getenv('COHERE_API_KEY')),
            'perplexity': bool(os.getenv('PERPLEXITY_API_KEY')),
        }
        
        available = [k for k, v in providers.items() if v]
        
        print("\n" + "="*60)
        print("🔍 API KEY TESPİTİ")
        print("="*60)
        for provider, available in providers.items():
            status = "✅ Mevcut" if available else "❌ Yok"
            print(f"{provider.upper():15} : {status}")
        print("="*60 + "\n")
        
        return providers
    
    def _generate_optimal_config(self) -> Dict:
        """Mevcut API key'lere göre optimal konfigürasyon"""
        
        # Hiç API key yoksa
        if not any(self.available_providers.values()):
            print("⚠️  UYARI: Hiç API key bulunamadı!")
            print("Demo modunda çalışılacak (AI yanıtları simüle edilecek)\n")
            return self._get_demo_config()
        
        # Sadece OpenAI varsa
        if self.available_providers['openai'] and sum(self.available_providers.values()) == 1:
            print("📌 Sadece OpenAI API key bulundu")
            print("Tüm çalışanlar OpenAI modelleri kullanacak\n")
            return self._get_openai_only_config()
        
        # OpenAI + Anthropic varsa (en yaygın)
        if self.available_providers['openai'] and self.available_providers['anthropic']:
            print("🎯 OpenAI + Anthropic tespit edildi")
            print("✨ AKILLI DAĞILIM:")
            print("   • Yazılım ekibi → Claude (daha iyi kod)")
            print("   • Marketing → GPT (daha kreatif)")
            print("   • Araştırma → Claude (daha derin analiz)")
            print("   • Executives → Claude Opus (karmaşık muhakeme)\n")
            return self._get_openai_anthropic_config()
        
        # Hepsi varsa
        if sum(self.available_providers.values()) >= 3:
            print("🌟 Çoklu AI sağlayıcı tespit edildi")
            print("En optimal dağılım yapılacak\n")
            return self._get_multi_provider_config()
        
        # Fallback
        return self._get_best_available_config()
    
    def _get_demo_config(self) -> Dict:
        """Demo modu - API key yok"""
        return {
            'mode': 'demo',
            'default_model': 'demo/simulated',
            'assignments': {
                'all': {
                    'primary': 'demo/simulated',
                    'fallback': 'demo/simulated',
                    'tier': 'demo'
                }
            }
        }
    
    def _get_openai_only_config(self) -> Dict:
        """Sadece OpenAI kullan"""
        return {
            'mode': 'openai-only',
            'default_model': 'gpt-4',
            'assignments': {
                'enterprise': {  # CEO, CTO, Lead roles
                    'primary': 'gpt-4-turbo-preview',
                    'fallback': 'gpt-4',
                    'tier': 'enterprise'
                },
                'pro': {  # Developers, Managers
                    'primary': 'gpt-4',
                    'fallback': 'gpt-3.5-turbo',
                    'tier': 'pro'
                },
                'basic': {  # Support, Junior roles
                    'primary': 'gpt-3.5-turbo',
                    'fallback': 'gpt-3.5-turbo',
                    'tier': 'basic'
                }
            }
        }
    
    def _get_openai_anthropic_config(self) -> Dict:
        """OpenAI + Anthropic optimal dağılım - Role bazlı akıllı seçim"""
        return {
            'mode': 'openai-anthropic',
            'default_model': 'gpt-4',
            'assignments': {
                'enterprise': {
                    'primary': 'claude-3-opus-20240229',  # Anthropic en güçlü
                    'fallback': 'gpt-4-turbo-preview',
                    'tier': 'enterprise'
                },
                'pro': {
                    'primary': 'gpt-4',
                    'fallback': 'claude-3-sonnet-20240229',
                    'tier': 'pro'
                },
                'basic': {
                    'primary': 'gpt-3.5-turbo',
                    'fallback': 'claude-3-haiku-20240307',
                    'tier': 'basic'
                }
            },
            # Role-specific overrides (güçlü yönlere göre)
            'role_overrides': {
                # CODING ROLES -> Claude (daha iyi kod üretir)
                'developer': 'claude-3-sonnet-20240229',
                'engineer': 'claude-3-sonnet-20240229',
                'programmer': 'claude-3-sonnet-20240229',
                'lead_developer': 'claude-3-opus-20240229',
                'senior_developer': 'claude-3-opus-20240229',
                'backend': 'claude-3-sonnet-20240229',
                'frontend': 'claude-3-sonnet-20240229',
                'ios': 'claude-3-sonnet-20240229',
                'android': 'claude-3-sonnet-20240229',
                'game_developer': 'claude-3-opus-20240229',
                
                # CREATIVE/MARKETING -> GPT (daha kreatif)
                'content_creator': 'gpt-4',
                'copywriter': 'gpt-4',
                'social_media': 'gpt-4',
                'graphic_designer': 'gpt-4',
                'marketing': 'gpt-4',
                
                # RESEARCH/ANALYSIS -> Claude (daha derin analiz)
                'researcher': 'claude-3-opus-20240229',
                'scientist': 'claude-3-opus-20240229',
                'analyst': 'claude-3-sonnet-20240229',
                'data_scientist': 'claude-3-sonnet-20240229',
                
                # EXECUTIVE/STRATEGY -> Claude Opus (karmaşık muhakeme)
                'ceo': 'claude-3-opus-20240229',
                'cto': 'claude-3-opus-20240229',
                'cfo': 'claude-3-opus-20240229',
                
                # SUPPORT -> GPT-3.5 (hızlı ve ucuz)
                'support': 'gpt-3.5-turbo',
                'agent': 'gpt-3.5-turbo'
            }
        }
    
    def _get_multi_provider_config(self) -> Dict:
        """Tüm provider'lar mevcut"""
        assignments = {}
        
        if self.available_providers['anthropic']:
            assignments['enterprise'] = {
                'primary': 'claude-3-opus-20240229',
                'fallback': 'gpt-4-turbo-preview',
                'tier': 'enterprise'
            }
        else:
            assignments['enterprise'] = {
                'primary': 'gpt-4-turbo-preview',
                'fallback': 'gpt-4',
                'tier': 'enterprise'
            }
        
        if self.available_providers['openai']:
            assignments['pro'] = {
                'primary': 'gpt-4',
                'fallback': 'claude-3-sonnet-20240229' if self.available_providers['anthropic'] else 'gpt-3.5-turbo',
                'tier': 'pro'
            }
        
        assignments['basic'] = {
            'primary': 'gpt-3.5-turbo',
            'fallback': 'claude-3-haiku-20240307' if , role_name: str = "") -> Dict:
        """Role zorluk seviyesi VE role tipine göre optimal model al"""
        config = self.optimal_config
        
        if config['mode'] == 'demo':
            return {
                'primary': 'demo/simulated',
                'fallback': 'demo/simulated',
                'tier': 'demo'
            }
        
        assignments = config['assignments']
        
        # Role-specific override kontrolü (OpenAI + Anthropic modunda)
        if 'role_overrides' in config and role_name:
            role_lower = role_name.lower()
            for key, model in config['role_overrides'].items():
                if key in role_lower:
                    # Override bulundu - role'e özgü en iyi AI
                    tier = 'enterprise' if role_difficulty >= 8 else 'pro' if role_difficulty >= 5 else 'basic'
                    fallback = assignments.get(tier, {}).get('fallback', config['default_model'])
                    return {
                        'primary': model,
                        'fallback': fallback,
                        'tier': tier,
                        'reason': f"Optimized for {key} role"
                    }
        
        # Zorluk seviyesine göre tier belirle (default)
                'mode': 'anthropic-only',
                'default_model': 'claude-3-sonnet-20240229',
                'assignments': {
                    'enterprise': {'primary': 'claude-3-opus-20240229', 'fallback': 'claude-3-sonnet-20240229', 'tier': 'enterprise'},
                    'pro': {'primary': 'claude-3-sonnet-20240229', 'fallback': 'claude-3-haiku-20240307', 'tier': 'pro'},
                    'basic': {'primary': 'claude-3-haiku-20240307', 'fallback': 'claude-3-haiku-20240307', 'tier': 'basic'}
                }
            }
        elif self.available_providers['google']:
            return {
                'mode': 'google-only',
                'default_model': 'gemini-pro',
                'assignments': {
                    'enterprise': {'primary': 'gemini-pro', 'fallback': 'gemini-pro', 'tier': 'enterprise'},
                    'pro': {'primary': 'gemini-pro', 'fallback': 'gemini-pro', 'tier': 'pro'},
                    'basic': {'primary': 'gemini-pro', 'fallback': 'gemini-pro', 'tier': 'basic'}
                }
            }
        
        # Final fallback
        return self._get_demo_config()
    
    def get_model_for_role(self, role_difficulty: int) -> Dict:
        """Role zorluk seviyesine göre model al"""
        config = self.optimal_config
        
        if config['mode'] == 'demo':
            return {
                'primary': 'demo/simulated',
                'fallback': 'demo/simulated',
                'tier': 'demo'
            }
        
        assignments = config['assignments']
        
        # Zorluk seviyesine göre tier belirle
        if role_difficulty >= 8:
            tier = 'enterprise'
        elif role_difficulty >= 5:
            tier = 'pro'
        else:
            tier = 'basic'
        
        return assignments.get(tier, assignments.get('pro', {'primary': config['default_model'], 'fallback': config['default_model'], 'tier': 'pro'}))
    
    def print_configuration_summary(self):
        """Konfigürasyon özetini yazdır"""
        print("\n" + "="*60)
        print("⚙️  OTOMATİK AI KONFİGÜRASYONU")
        print("="*60)
        print(f"Mod: {self.optimal_config['mode']}")
        print(f"Varsayılan Model: {self.optimal_config['default_model']}")
        print("\nTier Atamaları:")
        
        for tier, assignment in self.optimal_config.get('assignments', {}).items():
            if tier != 'all':
                print(f"\n  {tier.upper()}:")
                print(f"    Primary: {assignment['primary']}")
                print(f"    Fallback: {assignment['fallback']}")
        
        print("\n" + "="*60 + "\n")


# Global instance
_auto_configurator = None

def get_auto_configurator() -> AutoAIConfigurator:
    """Global auto configurator instance"""
    global _auto_configurator
    if _auto_configurator is None:
        _auto_configurator = AutoAIConfigurator()
    return _auto_configurator
