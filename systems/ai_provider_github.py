"""
AI Provider Manager - Çoklu AI sağlayıcı yönetimi
"""
from typing import Dict, Optional, List, Any
from enum import Enum
import yaml
import os
from dataclasses import dataclass
import asyncio
from systems.auto_config import get_auto_configurator



import logging
logger = logging.getLogger(__name__)
class AITier(str, Enum):
    """AI Tier seviyeleri"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class DifficultyLevel(int, Enum):
    """Görev zorluk seviyeleri"""
    VERY_EASY = 1
    EASY = 2
    SIMPLE = 3
    MODERATE = 4
    STANDARD = 5
    CHALLENGING = 6
    COMPLEX = 7
    VERY_COMPLEX = 8
    EXPERT = 9
    MASTER = 10


@dataclass
class AIModel:
    """AI Model bilgisi"""
    provider: str
    model_name: str
    tier: AITier
    cost: str
    strengths: List[str]
    best_for: List[str]
    context_window: int
    
    def __str__(self):
        return f"{self.provider}/{self.model_name}"


@dataclass
class RoleAIAssignment:
    """Role göre AI ataması"""
    role: str
    primary_ai: str
    fallback_ai: str
    tier: AITier
    difficulty_level: int
    reasoning: str


class AIProviderManager:
    """AI sağlayıcı yöneticisi"""
    , auto_mode: bool = True):
        self.auto_mode = auto_mode
        
        # Otomatik mod - API key'lere göre konfigüre et
        if auto_mode:
            self.auto_config = get_auto_configurator()
            self.auto_config.print_configuration_summary()
            self.config = {}
            self.providers = {}
            self.role_assignments = {}
            self.cost_optimization = {'daily_budget': 1000}
        else:
            # Manuel mod - YAML'dan yükle
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            self.providers: Dict[str, Dict] = self.config.get('ai_providers', {})
            self.role_assignments: Dict[str, Dict] = self.config.get('role_assignments', {})
            self.cost_optimization = self.config.get('cost_optimization', {})
            self.auto_config = Nonesignments', {})
        self.cost_optimization = self.config.get('cost_optimization', {})
        
        self.api_keys = self._load_api_keys()
        self.daily_cost = 0.0
        self.request_count = {}
    
    def _load_api_keys(self) -> Dict[str, str]:
        """API anahtarlarını yükle"""
        reOtomatik mod
        if self.auto_mode and self.auto_config:
            # Role zorluk seviyesini belirle
            difficulty = self._estimate_role_difficulty(role)
            model_config = self.auto_config.get_model_for_role(difficulty, role)
            
            reason = model_config.get('reason', f"Auto-configured (difficulty: {difficulty})")
            
            return RoleAIAssignment(
                role=role,
                primary_ai=model_config['primary'],
                fallback_ai=model_config['fallback'],
                tier=AITier(model_config['tier']),
                difficulty_level=difficulty,
                reasoning=reason
            )
        
        # Manuel mod - Departman içinde rol ara
        if department and department in self.role_assignments:
            dept_config = self.role_assignments[department]
            
            # Role'ü normalize et (snake_case)
            role_key = role.lower().replace(' ', '_').replace('/', '_')
            
            if role_key in dept_config:
                config = dept_config[role_key]
                return RoleAIAssignment(
                    role=role,
                    primary_ai=config['primary_ai'],
                    fallback_ai=config['fallback_ai'],
                    tier=AITier(config['tier']),
                    difficulty_level=config['difficulty_level'],
                    reasoning=config['reasoning']
                )
        
        # Varsayılan AI
        return self._get_default_assignment(role)
    
    def _estimate_role_difficulty(self, role: str) -> int:
        """Role'e göre zorluk seviyesi tahmin et"""
        role_lower = role.lower()
        
        # Executive/Leadership roles (9-10)
        if any(x in role_lower for x in ['ceo', 'cto', 'cfo', 'chief', 'vp', 'director']):
            return 9
        
        # Senior/Lead roles (7-9)
        if any(x in role_lower for x in ['lead', 'senior', 'architect', 'principal']):
            return 8
        
        # Specialist/Expert roles (6-7)
        if any(x in role_lower for x in ['scientist', 'researcher', 'specialist']):
            return 7
        
        # Manager roles (6-7)
        if 'manager' in role_lower:
            return 7
        
        # Developer/Engineer roles (5-7)
        if any(x in role_lower for x in ['developer', 'engineer', 'programmer']):
            return 6
        
        # Designer/Analyst roles (5-6)
        if any(x in role_lower for x in ['designer', 'analyst', 'writer']):
            return 5
        
        # Support/Junior roles (3-4)
        if any(x in role_lower for x in ['support', 'agent', 'assistant', 'junior']):
            return 3
        
        # Default
        return 5
    
    def _get_default_assignment(self, role: str) -> RoleAIAssignment:
        """Varsayılan AI ataması"""
        if self.auto_mode and self.auto_config:, role)
            
            reason = model_config.get('reason', "Auto-configured default")
            
            return RoleAIAssignment(
                role=role,
                primary_ai=model_config['primary'],
                fallback_ai=model_config['fallback'],
                tier=AITier(model_config['tier']),
                difficulty_level=difficulty,
                reasoning=reason
                difficulty_level=difficulty,
                reasoning="Auto-configured default"
            )
        
        return RoleAIAssignment(
            role=role,
            primary_ai="gpt-4",
            fallback_ai="gpt-3.5-turbo",
            tier=AITier.PRO,
            difficulty_level=5,
            reasoning="Fallback d=AITier(config['tier']),
                    difficulty_level=config['difficulty_level'],
                    reasoning=config['reasoning']
                )
        
        # Varsayılan AI (eğer bulunamazsa)
        return RoleAIAssignment(
            role=role,
            primary_ai="openai/gpt-4",
            fallback_ai="anthropic/claude-3-sonnet",
            tier=AITier.PRO,
            difficulty_level=5,
            reasoning="Default assignment"
        )
    
    def get_model_info(self, model_path: str) -> Optional[AIModel]:
        """Model bilgisini al (örn: 'openai/gpt-4-turbo')"""
        try:
            provider, model_name = model_path.split('/')
            
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
            # Demo mode
            if model_path == 'demo/simulated':
                return self._create_demo_client()
            
            # Normal provider/model format
            if '/' in model_path:
                provider, model_name = model_path.split('/', 1)
            else:
                # Sadece model ismi verilmişse, OpenAI varsay
                provider = 'openai'
                model_name = model_path
            
            if provider == 'openai':
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model=model_name,
                    api_key=self.api_keys['openai'],
                    temperature=0.7
                )
            
            elif provider == 'anthropic':
                from langchain_anthropic import ChatAnthropic
                return ChatAnthropic(
                    model=model_name,
                    api_key=self.api_keys['anthropic'],
                    temperature=0.7
                )
            
            elif provider == 'google':
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=self.api_keys['google'],
                    temperature=0.7
                )
            
            # Diğer provider'lar için fallback
            else:
                logger.info(f"⚠️ {provider} desteklenmiyor, mevcut provider kullanılıyor")
                return self._create_fallback_client()
                
        except Exception as e:
            logger.info(f"⚠️ LLM client oluşturulamadı: {e}, fallback kullanılıyor")
            return self._create_fallback_client()
    
    def _create_fallback_client(self):
        """En iyi mevcut client'ı oluştur"""
        if self.api_keys['openai']:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model="gpt-3.5-turbo", api_key=self.api_keys['openai'], temperature=0.7)
        elif self.api_keys['anthropic']:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model="claude-3-haiku-20240307", api_key=self.api_keys['anthropic'], temperature=0.7)
        else:
            return self._create_demo_client()
    
    def _create_demo_client(self):
        """Demo client - API key olmadan"""
        from langchain.schema import HumanMessage, AIMessage
        
        class DemoLLM:
            async def ainvoke(self, messages):
                return AIMessage(content="[Demo Mode] Bu bir simülasyon yanıtıdır. Gerçek AI yanıtı için API key ekleyin.")
        
        return DemoLLM(l_info = self.get_model_info(selected_ai)
        
        return {
            'selected_ai': selected_ai,
            'model_info': model_info,
            'assignment': assignment,
            'reason': self._get_selection_reason(assignment, task_difficulty)
        }
    
    def _get_selection_reason(self, assignment: RoleAIAssignment, task_difficulty: int) -> str:
        """Seçim nedenini açıkla"""
        if task_difficulty >= 8:
            return f"Kritik görev (zorluk {task_difficulty}) - En güçlü AI kullanılıyor"
        elif task_difficulty < assignment.difficulty_level - 2:
            return f"Basit görev (zorluk {task_difficulty}) - Maliyet optimizasyonu için fallback AI"
        elif self.daily_cost > self.cost_optimization.get('daily_budget', 1000) * 0.8:
            return "Bütçe limiti yaklaşıyor - Fallback AI kullanılıyor"
        else:
            return f"Standart görev (zorluk {task_difficulty}) - Primary AI kullanılıyor"
    
    def create_llm_client(self, model_path: str):
        """LLM client oluştur"""
        try:
            provider, model_name = model_path.split('/')
            
            if provider == 'openai':
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model=model_name,
                    api_key=self.api_keys['openai'],
                    temperature=0.7
                )
            
            elif provider == 'anthropic':
                from langchain_anthropic import ChatAnthropic
                return ChatAnthropic(
                    model=model_name,
                    api_key=self.api_keys['anthropic'],
                    temperature=0.7
                )
            
            elif provider == 'google':
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=self.api_keys['google'],
                    temperature=0.7
                )
            
            # Diğer provider'lar için fallback
            else:
                logger.info(f"⚠️ {provider} desteklenmiyor, OpenAI kullanılıyor")
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model="gpt-4",
                    api_key=self.api_keys['openai'],
                    temperature=0.7
                )
                
        except Exception as e:
            logger.info(f"❌ LLM client oluşturulamadı: {e}")
            # Fallback to GPT-3.5
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=self.api_keys['openai'],
                temperature=0.7
            )
    
    def generate_ai_assignment_report(self) -> str:
        """AI atama raporunu oluştur"""
        report = f"""
{'='*80}
🤖 AI PROVIDER ATAMA RAPORU
{'='*80}

📊 MEVCUT AI PROVIDERS:
"""
        
        # Provider'ları listele
        for provider, data in self.providers.items():
            models = data.get('models', {})
            report += f"\n{provider.upper()}:\n"
            for model_name, model_data in models.items():
                report += f"  • {model_name} ({model_data['tier']}) - {model_data['cost']}\n"
        
        report += f"\n{'='*80}\n"
        report += "👥 ROLE-BASED AI ASSIGNMENTS:\n\n"
        
        # Departman bazlı atamaları göster
        for dept, roles in self.role_assignments.items():
            report += f"\n📁 {dept.upper()}:\n"
            for role, config in roles.items():
                report += f"  • {role}:\n"
                report += f"    Primary: {config['primary_ai']}\n"
                report += f"    Tier: {config['tier']}\n"
                report += f"    Difficulty: {config['difficulty_level']}/10\n"
                report += f"    Reason: {config['reasoning']}\n"
        
        report += f"\n{'='*80}\n"
        report += "💰 COST OPTIMIZATION:\n"
        for rule in self.cost_optimization.get('rules', []):
            report += f"  • {rule}\n"
        
        report += f"\n{'='*80}\n"
        
        return report
    
    def get_tier_statistics(self) -> Dict:
        """Tier istatistiklerini al"""
        stats = {
            'free': 0,
            'basic': 0,
            'pro': 0,
            'enterprise': 0
        }
        
        for dept, roles in self.role_assignments.items():
            for role, config in roles.items():
                tier = config['tier']
                stats[tier] = stats.get(tier, 0) + 1
        
        return stats
