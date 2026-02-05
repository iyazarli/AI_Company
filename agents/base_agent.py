"""
Base Agent Class - Tüm AI çalışanların temel sınıfı
"""
from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
import asyncio
from abc import ABC, abstractmethod



import logging
logger = logging.getLogger(__name__)
class Task(BaseModel):
    """Görev modeli"""
    id: str
    title: str
    description: str
    assigned_to: str
    assigned_by: str
    department: str
    priority: str = "medium"  # low, medium, high, critical
    status: str = "pending"  # pending, in_progress, completed, blocked
    created_at: datetime = Field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    dependencies: List[str] = []
    result: Optional[str] = None
    

class Message(BaseModel):
    """Mesaj modeli"""
    id: str
    from_agent: str
    to_agent: str
    subject: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    read: bool = False


class AgentMemory(BaseModel):
    """Agent hafızası"""
    tasks_completed: List[Task] = []
    tasks_active: List[Task] = []
    messages_sent: List[Message] = []
    messages_received: List[Message] = []
    meetings_attended: List[Dict] = []
    decisions_made: List[Dict] = []


class BaseAgent(ABC):
    """Tüm AI ajanların temel sınıfı"""
    
    def __init__(
        self,
        name: str,
        role: str,
        department: str,
        skills: List[str],
        manager: Optional[str] = None,
        llm_config: Optional[Dict] = None
    ):
        self.name = name
        self.role = role
        self.department = department
        self.skills = skills
        self.manager = manager
        self.llm_config = llm_config or {}
        
        self.memory = AgentMemory()
        self.is_active = True
        self.current_task: Optional[Task] = None
        self.performance_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "response_time_avg": 0.0,
            "quality_score": 0.0
        }
    
    async def receive_task(self, task: Task) -> bool:
        """Görev al"""
        if task.assigned_to == self.name:
            self.memory.tasks_active.append(task)
            logger.info(f"✅ {self.name} ({self.role}) - Yeni görev alındı: {task.title}")
            return True
        return False
    
    async def complete_task(self, task_id: str, result: str) -> bool:
        """Görevi tamamla"""
        for task in self.memory.tasks_active:
            if task.id == task_id:
                task.status = "completed"
                task.result = result
                self.memory.tasks_completed.append(task)
                self.memory.tasks_active.remove(task)
                self.performance_metrics["tasks_completed"] += 1
                logger.info(f"✅ {self.name} - Görev tamamlandı: {task.title}")
                return True
        return False
    
    async def send_message(self, to_agent: str, subject: str, content: str) -> Message:
        """Mesaj gönder"""
        message = Message(
            id=f"msg_{datetime.now().timestamp()}",
            from_agent=self.name,
            to_agent=to_agent,
            subject=subject,
            content=content
        )
        self.memory.messages_sent.append(message)
        return message
    
    async def receive_message(self, message: Message) -> bool:
        """Mesaj al"""
        if message.to_agent == self.name:
            self.memory.messages_received.append(message)
            logger.info(f"📨 {self.name} - Yeni mesaj: {message.subject} (from: {message.from_agent})")
            return True
        return False
    
    async def attend_meeting(self, meeting_info: Dict) -> Dict:
        """Toplantıya katıl"""
        self.memory.meetings_attended.append(meeting_info)
        contribution = await self.generate_meeting_contribution(meeting_info)
        return contribution
    
    @abstractmethod
    async def execute_task(self, task: Task) -> str:
        """Görevi yürüt - Her agent kendi implementasyonunu yapar"""
        pass
    
    @abstractmethod
    async def generate_meeting_contribution(self, meeting_info: Dict) -> Dict:
        """Toplantıda katkı sağla"""
        pass
    
    async def daily_standup_update(self) -> Dict:
        """Günlük standup güncellesi"""
        yesterday_tasks = [
            t for t in self.memory.tasks_completed 
            if (datetime.now() - t.created_at).days < 1
        ]
        
        return {
            "agent": self.name,
            "role": self.role,
            "yesterday": [t.title for t in yesterday_tasks],
            "today": [t.title for t in self.memory.tasks_active],
            "blockers": [
                t.title for t in self.memory.tasks_active 
                if t.status == "blocked"
            ]
        }
    
    async def get_status(self) -> Dict:
        """Agent durumunu al"""
        return {
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "is_active": self.is_active,
            "current_task": self.current_task.title if self.current_task else None,
            "active_tasks": len(self.memory.tasks_active),
            "completed_tasks": len(self.memory.tasks_completed),
            "unread_messages": len([m for m in self.memory.messages_received if not m.read]),
            "performance": self.performance_metrics
        }
    
    async def think(self, context: str) -> str:
        """AI düşünme/karar verme - LLM ile"""
        # Bu method LLM entegrasyonu ile implement edilecek
        # Şimdilik basit bir placeholder
        return f"{self.name} analyzing: {context}"
    
    async def work_cycle(self):
        """Sürekli çalışma döngüsü"""
        while self.is_active:
            # Aktif görevleri kontrol et
            if self.memory.tasks_active:
                for task in self.memory.tasks_active:
                    if task.status == "pending":
                        task.status = "in_progress"
                        self.current_task = task
                        result = await self.execute_task(task)
                        await self.complete_task(task.id, result)
                        self.current_task = None
            
            # Mesajları kontrol et
            unread = [m for m in self.memory.messages_received if not m.read]
            for msg in unread:
                await self.process_message(msg)
                msg.read = True
            
            # Kısa bekleme
            await asyncio.sleep(5)
    
    async def process_message(self, message: Message):
        """Mesajı işle"""
        logger.info(f"📖 {self.name} - Mesaj okunuyor: {message.subject}")
        # Mesaja göre aksiyon al
        pass
    
    def __repr__(self):
        return f"<Agent: {self.name} ({self.role}) - {self.department}>"
