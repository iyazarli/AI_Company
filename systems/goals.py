"""
Goal Management System - Hedef belirleme ve takip sistemi
"""
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum



import logging
logger = logging.getLogger(__name__)
class GoalPeriod(str, Enum):
    """Hedef periyodu"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class GoalStatus(str, Enum):
    """Hedef durumu"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Goal(BaseModel):
    """Hedef modeli"""
    id: str
    title: str
    description: str
    period: GoalPeriod
    status: GoalStatus = GoalStatus.NOT_STARTED
    owner: Optional[str] = None  # CEO, CTO, department name, etc.
    department: Optional[str] = None
    created_at: datetime = datetime.now()
    deadline: Optional[datetime] = None
    progress: float = 0.0  # 0-100
    metrics: Dict = {}
    sub_goals: List[str] = []


class GoalManager:
    """Hedef yönetim sistemi"""
    
    def __init__(self):
        self.goals: Dict[str, Goal] = {}
        self.active_goals: List[Goal] = []
        self.completed_goals: List[Goal] = []
    
    def set_company_goal(
        self,
        title: str,
        description: str,
        period: GoalPeriod,
        owner: str = "CEO",
        deadline: Optional[datetime] = None,
        metrics: Dict = None
    ) -> Goal:
        """Şirket hedefi belirle"""
        goal = Goal(
            id=f"goal_{datetime.now().timestamp()}",
            title=title,
            description=description,
            period=period,
            owner=owner,
            deadline=deadline,
            metrics=metrics or {}
        )
        
        self.goals[goal.id] = goal
        self.active_goals.append(goal)
        
        logger.info(f"\n🎯 YENİ HEDEF BELİRLENDİ")
        logger.info(f"   📌 {title}")
        logger.info(f"   👤 Sorumlu: {owner}")
        logger.info(f"   📅 Periyod: {period.value}")
        if deadline:
            logger.info(f"   ⏰ Son Tarih: {deadline.strftime('%Y-%m-%d')}")
        print()
        
        return goal
    
    def set_department_goal(
        self,
        department: str,
        title: str,
        description: str,
        period: GoalPeriod,
        owner: str,
        deadline: Optional[datetime] = None
    ) -> Goal:
        """Departman hedefi belirle"""
        goal = Goal(
            id=f"goal_{department}_{datetime.now().timestamp()}",
            title=title,
            description=description,
            period=period,
            owner=owner,
            department=department,
            deadline=deadline
        )
        
        self.goals[goal.id] = goal
        self.active_goals.append(goal)
        
        logger.info(f"\n🎯 DEPARTMAN HEDEFİ: {department}")
        logger.info(f"   📌 {title}")
        logger.info(f"   👤 Sorumlu: {owner}")
        print()
        
        return goal
    
    def update_goal_progress(self, goal_id: str, progress: float, notes: str = ""):
        """Hedef ilerlemesini güncelle"""
        if goal_id in self.goals:
            goal = self.goals[goal_id]
            old_progress = goal.progress
            goal.progress = min(100.0, max(0.0, progress))
            
            logger.info(f"📊 Hedef İlerlemesi Güncellendi: {goal.title}")
            logger.info(f"   {old_progress:.1f}% -> {goal.progress:.1f}%")
            if notes:
                logger.info(f"   💬 {notes}")
            
            # Tamamlanma kontrolü
            if goal.progress >= 100.0 and goal.status != GoalStatus.COMPLETED:
                self.complete_goal(goal_id)
    
    def complete_goal(self, goal_id: str):
        """Hedefi tamamla"""
        if goal_id in self.goals:
            goal = self.goals[goal_id]
            goal.status = GoalStatus.COMPLETED
            goal.progress = 100.0
            
            if goal in self.active_goals:
                self.active_goals.remove(goal)
            self.completed_goals.append(goal)
            
            logger.info(f"\n✅ HEDEF TAMAMLANDI: {goal.title}")
            logger.info(f"   👏 Tebrikler! {goal.owner}")
            print()
    
    def get_active_goals(self, period: Optional[GoalPeriod] = None) -> List[Goal]:
        """Aktif hedefleri al"""
        if period:
            return [g for g in self.active_goals if g.period == period]
        return self.active_goals
    
    def get_department_goals(self, department: str) -> List[Goal]:
        """Departman hedeflerini al"""
        return [g for g in self.goals.values() if g.department == department]
    
    def get_goal_report(self) -> str:
        """Hedef raporu oluştur"""
        report = f"""
{'='*60}
🎯 HEDEF RAPORU - {datetime.now().strftime('%Y-%m-%d')}
{'='*60}

📊 Genel Durum:
   • Toplam Hedef: {len(self.goals)}
   • Aktif: {len(self.active_goals)}
   • Tamamlanan: {len(self.completed_goals)}
   • Tamamlanma Oranı: %{(len(self.completed_goals) / len(self.goals) * 100) if self.goals else 0:.1f}

"""
        
        # Periyoda göre hedefler
        for period in GoalPeriod:
            period_goals = [g for g in self.active_goals if g.period == period]
            if period_goals:
                report += f"\n📅 {period.value.upper()} Hedefleri:\n"
                for goal in period_goals:
                    report += f"   • {goal.title} - %{goal.progress:.0f} ({goal.owner})\n"
        
        # Tamamlanan son 5 hedef
        if self.completed_goals:
            report += f"\n✅ Son Tamamlanan Hedefler:\n"
            for goal in self.completed_goals[-5:]:
                report += f"   • {goal.title} ({goal.owner})\n"
        
        report += f"\n{'='*60}\n"
        return report
    
    def load_goals_from_config(self, config: Dict):
        """Config'den hedefleri yükle"""
        goals_config = config.get('company', {}).get('goals', {})
        
        # Quarterly goals
        for goal_title in goals_config.get('quarterly', []):
            self.set_company_goal(
                title=goal_title,
                description=f"Q1 2026 hedefi: {goal_title}",
                period=GoalPeriod.QUARTERLY,
                owner="CEO"
            )
        
        # Monthly goals
        for goal_title in goals_config.get('monthly', []):
            self.set_company_goal(
                title=goal_title,
                description=f"Aylık hedef: {goal_title}",
                period=GoalPeriod.MONTHLY,
                owner="CEO"
            )
        
        # Weekly goals
        for goal_title in goals_config.get('weekly', []):
            self.set_company_goal(
                title=goal_title,
                description=f"Haftalık hedef: {goal_title}",
                period=GoalPeriod.WEEKLY,
                owner="Management"
            )


class GoalSettingInterface:
    """İnteraktif hedef belirleme arayüzü"""
    
    def __init__(self, goal_manager: GoalManager):
        self.goal_manager = goal_manager
    
    def interactive_goal_setting(self):
        """İnteraktif hedef belirleme"""
        logger.info("\n" + "="*60)
        print("🎯 ŞİRKET HEDEFİ BELİRLEME")
        logger.info("="*60 + "\n")
        
        title = input("Hedef Başlığı: ")
        description = input("Açıklama: ")
        
        logger.info("\nPeriyod Seçin:")
        logger.info("1. Günlük")
        logger.info("2. Haftalık")
        logger.info("3. Aylık")
        logger.info("4. Üç Aylık")
        logger.info("5. Yıllık")
        
        period_choice = input("\nSeçim (1-5): ").strip()
        period_map = {
            "1": GoalPeriod.DAILY,
            "2": GoalPeriod.WEEKLY,
            "3": GoalPeriod.MONTHLY,
            "4": GoalPeriod.QUARTERLY,
            "5": GoalPeriod.YEARLY
        }
        period = period_map.get(period_choice, GoalPeriod.MONTHLY)
        
        owner = input("Sorumlu (CEO, CTO, department adı, vb.): ") or "CEO"
        
        # Hedefi oluştur
        goal = self.goal_manager.set_company_goal(
            title=title,
            description=description,
            period=period,
            owner=owner
        )
        
        logger.info(f"✅ Hedef başarıyla oluşturuldu! (ID: {goal.id})")
        return goal
    
    def quick_set_goals(self, goals: List[Dict]):
        """Hızlı hedef belirleme - Liste ile"""
        logger.info("\n🚀 Toplu Hedef Belirleme Başlıyor...\n")
        
        created_goals = []
        for goal_data in goals:
            goal = self.goal_manager.set_company_goal(
                title=goal_data.get('title'),
                description=goal_data.get('description', ''),
                period=GoalPeriod(goal_data.get('period', 'monthly')),
                owner=goal_data.get('owner', 'CEO')
            )
            created_goals.append(goal)
        
        logger.info(f"\n✅ {len(created_goals)} hedef belirlendi!\n")
        return created_goals
