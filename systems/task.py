"""
Task Management System - Görev yönetim sistemi
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import uuid
from agents.base_agent import Task
from agents.ai_agent import AIAgent, ManagerAgent


class TaskPriority:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskManager:
    """Görev yönetim sistemi"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
    
    def create_task(
        self,
        title: str,
        description: str,
        assigned_to: str,
        assigned_by: str,
        department: str,
        priority: str = TaskPriority.MEDIUM,
        deadline: Optional[datetime] = None,
        dependencies: List[str] = None
    ) -> Task:
        """Yeni görev oluştur"""
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            assigned_to=assigned_to,
            assigned_by=assigned_by,
            department=department,
            priority=priority,
            deadline=deadline or datetime.now() + timedelta(days=7),
            dependencies=dependencies or []
        )
        
        self.tasks[task.id] = task
        self.task_queue.append(task)
        
        print(f"📋 Yeni görev oluşturuldu: {title}")
        print(f"   👤 Atanan: {assigned_to}")
        print(f"   ⚡ Öncelik: {priority}")
        print(f"   📅 Son tarih: {task.deadline.strftime('%Y-%m-%d')}")
        
        return task
    
    async def assign_task_to_agent(self, task: Task, agent: AIAgent) -> bool:
        """Görevi agenta ata"""
        success = await agent.receive_task(task)
        if success:
            task.status = TaskStatus.PENDING
            print(f"✅ Görev atandı: {task.title} -> {agent.name}")
        return success
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """Görev durumunu güncelle"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            old_status = task.status
            task.status = status
            
            if status == TaskStatus.COMPLETED:
                self.completed_tasks.append(task)
                if task in self.task_queue:
                    self.task_queue.remove(task)
            
            print(f"🔄 Görev durumu güncellendi: {task.title}")
            print(f"   {old_status} -> {status}")
            return True
        return False
    
    def get_agent_tasks(self, agent_name: str) -> List[Task]:
        """Agentin görevlerini al"""
        return [t for t in self.tasks.values() if t.assigned_to == agent_name]
    
    def get_pending_tasks(self) -> List[Task]:
        """Bekleyen görevleri al"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
    
    def get_in_progress_tasks(self) -> List[Task]:
        """Devam eden görevleri al"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]
    
    def get_blocked_tasks(self) -> List[Task]:
        """Bloke olan görevleri al"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.BLOCKED]
    
    def get_overdue_tasks(self) -> List[Task]:
        """Gecikmiş görevleri al"""
        now = datetime.now()
        return [
            t for t in self.tasks.values() 
            if t.deadline < now and t.status != TaskStatus.COMPLETED
        ]
    
    def get_high_priority_tasks(self) -> List[Task]:
        """Yüksek öncelikli görevleri al"""
        return [
            t for t in self.tasks.values() 
            if t.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]
            and t.status != TaskStatus.COMPLETED
        ]
    
    def get_department_tasks(self, department: str) -> List[Task]:
        """Departman görevlerini al"""
        return [t for t in self.tasks.values() if t.department == department]
    
    def get_task_statistics(self) -> Dict:
        """Görev istatistikleri"""
        total = len(self.tasks)
        completed = len(self.completed_tasks)
        pending = len(self.get_pending_tasks())
        in_progress = len(self.get_in_progress_tasks())
        blocked = len(self.get_blocked_tasks())
        overdue = len(self.get_overdue_tasks())
        
        return {
            "total_tasks": total,
            "completed": completed,
            "pending": pending,
            "in_progress": in_progress,
            "blocked": blocked,
            "overdue": overdue,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }
    
    async def auto_assign_tasks(
        self,
        manager: ManagerAgent,
        available_agents: List[AIAgent]
    ) -> List[Task]:
        """Yöneticinin otomatik görev ataması yapması"""
        assigned_tasks = []
        
        # Yöneticiden görev planı iste
        sprint_plan = await manager.plan_sprint(duration_weeks=2)
        
        print(f"\n📊 {manager.name} sprint planı oluşturdu:")
        print(f"{sprint_plan['plan']}\n")
        
        # Basit oto-atama: Her agenta bir görev
        for i, agent in enumerate(available_agents):
            task = self.create_task(
                title=f"Sprint Task {i+1} for {agent.role}",
                description=f"Task aligned with sprint goals for {agent.role}",
                assigned_to=agent.name,
                assigned_by=manager.name,
                department=agent.department,
                priority=TaskPriority.MEDIUM
            )
            
            await self.assign_task_to_agent(task, agent)
            assigned_tasks.append(task)
        
        return assigned_tasks
    
    def generate_task_report(self) -> str:
        """Görev raporu oluştur"""
        stats = self.get_task_statistics()
        
        report = f"""
{'='*60}
GÖREV RAPORU
{'='*60}

📊 Genel Durum:
   Toplam Görev: {stats['total_tasks']}
   ✅ Tamamlanan: {stats['completed']}
   ⏳ Bekleyen: {stats['pending']}
   🔄 Devam Eden: {stats['in_progress']}
   ⛔ Bloke: {stats['blocked']}
   ⚠️  Gecikmiş: {stats['overdue']}
   
📈 Tamamlanma Oranı: %{stats['completion_rate']:.1f}

🔥 Yüksek Öncelikli Görevler:
"""
        
        high_priority = self.get_high_priority_tasks()
        for task in high_priority[:5]:  # İlk 5'i göster
            report += f"   • {task.title} ({task.assigned_to}) - {task.priority}\n"
        
        report += f"\n{'='*60}\n"
        
        return report
