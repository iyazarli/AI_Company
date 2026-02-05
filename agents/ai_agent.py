"""
AI-Powered Agents - LLM entegrasyonlu ajanlar
"""
from typing import List, Dict, Optional
from agents.base_agent import BaseAgent, Task
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import os
from systems.ai_provider import AIProviderManager


class AIAgent(BaseAgent):
    """LLM destekli AI Agent"""
    
    def __init__(self, name: str, role: str, department: str, skills: List[str], 
                 manager: Optional[str] = None, model: str = None, 
                 ai_provider_manager: AIProviderManager = None):
        super().__init__(name, role, department, skills, manager)
        
        # AI Provider Manager
        self.ai_provider_manager = ai_provider_manager or AIProviderManager()
        
        # Role'e göre en uygun AI'ı seç
        if model:
            # Manuel model belirtilmişse onu kullan
            self.assigned_ai = model
            self.llm = ChatOpenAI(
                model=model,
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        else:
            # Role'e göre otomatik AI seçimi
            assignment = self.ai_provider_manager.get_ai_for_role(role, department)
            self.assigned_ai = assignment.primary_ai
            self.fallback_ai = assignment.fallback_ai
            self.ai_tier = assignment.tier
            self.difficulty_level = assignment.difficulty_level
            
            # LLM client oluştur
            self.llm = self.ai_provider_manager.create_llm_client(self.assigned_ai)
            
            print(f"🤖 {name} -> {self.assigned_ai} ({self.ai_tier.value})")
        
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Agent için sistem promptu oluştur"""
        return f"""Sen {self.name} adında bir AI çalışansın.
Rolün: {self.role}
Departman: {self.department}
Yeteneklerin: {', '.join(self.skills)}
Yöneticin: {self.manager or 'Yok'}

Görevlerin:
1. Verilen görevleri profesyonelce ve etkili şekilde tamamla
2. Diğer departmanlarla iş birliği yap
3. Günlük standup toplantılarına katıl
4. Yöneticine düzenli rapor ver
5. Şirket hedeflerine ulaşmak için çalış

Her zaman:
- Profesyonel ol
- Detaylı ve açıklayıcı cevaplar ver
- Sorunları proaktif şekilde çöz
- Takım çalışmasına önem ver
- Yüksek kaliteli iş üret

Sen gerçek bir çalışan gibi davran ve verilen görevleri en iyi şekilde tamamla."""

    async def execute_task(self, task: Task) -> str:
        """Görevi AI ile yürüt"""
        prompt = f"""
Görev: {task.title}
Açıklama: {task.description}
Öncelik: {task.priority}
Son Tarih: {task.deadline}

Bu görevi senin yeteneklerin ({', '.join(self.skills)}) kullanarak tamamla.
Detaylı bir çözüm üret ve sonucu açıkla.
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        result = response.content
        
        print(f"🎯 {self.name} - Görev tamamlandı: {task.title}")
        return result
    
    async def generate_meeting_contribution(self, meeting_info: Dict) -> Dict:
        """Toplantı katkısı oluştur"""
        meeting_type = meeting_info.get("type", "general")
        agenda = meeting_info.get("agenda", [])
        
        prompt = f"""
Toplantı Türü: {meeting_type}
Gündem: {', '.join(agenda)}

Sen {self.role} olarak bu toplantıya katılıyorsun.
Departmanın ({self.department}) perspektifinden:
1. Güncel durum güncellemesi yap
2. Önemli konuları paylaş
3. Diğer departmanlarla koordinasyon gerektiren konuları belirt
4. Öneriler sun

Kısa ve öz bir katkı hazırla.
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            "agent": self.name,
            "role": self.role,
            "contribution": response.content
        }
    
    async def make_decision(self, context: str, options: List[str]) -> Dict:
        """Karar ver"""
        prompt = f"""
Karar Vermem Gereken Durum:
{context}

Seçenekler:
{chr(10).join([f"{i+1}. {opt}" for i, opt in enumerate(options)])}

Senin rolün ({self.role}) ve yeteneklerin göz önüne alarak:
1. En iyi seçeneği belirle
2. Nedenini açıkla
3. Potansiyel riskleri değerlendir
4. Aksiyon planı öner

JSON formatında cevap ver:
{{
    "decision": "seçilen seçenek",
    "reasoning": "karar gerekçesi",
    "risks": ["risk1", "risk2"],
    "action_plan": ["adım1", "adım2"]
}}
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            "agent": self.name,
            "decision_context": context,
            "decision_output": response.content
        }
    
    async def collaborate(self, other_agent: str, topic: str) -> str:
        """Başka bir ajanla iş birliği yap"""
        prompt = f"""
{other_agent} ile {topic} konusunda iş birliği yapman gerekiyor.

Senin rolün: {self.role}
Karşı tarafın rolü: {other_agent}

1. Bu konuda nasıl katkı sağlayabilirsin?
2. Karşı taraftan ne tür bilgi/destek bekliyorsun?
3. İş birliği planı öner
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        return response.content


class ManagerAgent(AIAgent):
    """Yönetici AI Agent - Görev verme yetkisi var"""
    
    def __init__(self, name: str, role: str, department: str, skills: List[str], 
                 team_members: List[str] = None, ai_provider_manager = None):
        super().__init__(name, role, department, skills, ai_provider_manager=ai_provider_manager)
        self.team_members = team_members or []
        self.is_manager = True
    
    async def assign_task(self, task: Task, assignee: str) -> bool:
        """Takım üyesine görev ata"""
        if assignee in self.team_members:
            task.assigned_by = self.name
            task.assigned_to = assignee
            print(f"📋 {self.name} -> {assignee}: Yeni görev atandı - {task.title}")
            return True
        return False
    
    async def review_team_performance(self) -> Dict:
        """Takım performansını değerlendir"""
        prompt = f"""
Sen {self.role} olarak takımının performansını değerlendiriyorsun.

Takım Üyeleri: {', '.join(self.team_members)}

1. Genel performans değerlendirmesi yap
2. Güçlü yönleri belirt
3. İyileştirme alanları öner
4. Önümüzdeki dönem için hedefler belirle
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            "manager": self.name,
            "team": self.team_members,
            "review": response.content
        }
    
    async def plan_sprint(self, duration_weeks: int = 2) -> Dict:
        """Sprint planla"""
        prompt = f"""
{duration_weeks} haftalık bir sprint planla.

Departman: {self.department}
Takım: {', '.join(self.team_members)}

Sprint için:
1. Hedefler belirle
2. Görevleri önceliklendir
3. Takım üyelerine görev dağılımı öner
4. Başarı metriklerini tanımla
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            "sprint_planner": self.name,
            "duration": f"{duration_weeks} weeks",
            "plan": response.content
        }


class ExecutiveAgent(ManagerAgent):
    """C-Level Executive AI Agent - Stratejik kararlar alır"""
    
    def __init__(self, name: str, role: str, department: str, skills: List[str],
                 ai_provider_manager = None):
        super().__init__(name, role, department, skills, ai_provider_manager=ai_provider_manager)
        self.is_executive = True
    
    async def make_strategic_decision(self, situation: str) -> Dict:
        """Stratejik karar al"""
        prompt = f"""
Sen {self.role} olarak şirket için stratejik bir karar alman gerekiyor.

Durum:
{situation}

C-level perspektiften:
1. Durumu analiz et
2. Stratejik seçenekleri değerlendir
3. Şirket vizyonu ile uyumlu kararı al
4. Uygulama planı oluştur
5. Riskleri ve fırsatları belirt
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            "executive": self.name,
            "decision_type": "strategic",
            "decision": response.content
        }
    
    async def quarterly_review(self) -> Dict:
        """Üç aylık değerlendirme"""
        prompt = """
Çeyrek dönem değerlendirmesi yap:
1. Hedeflere ulaşım durumu
2. Finansal performans
3. Takım performansı
4. Pazar durumu
5. Gelecek çeyrek stratejisi
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            "executive": self.name,
            "review_type": "quarterly",
            "review": response.content
        }
