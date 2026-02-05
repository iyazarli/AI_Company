"""
Company Core - Ana şirket sınıfı ve yönetimi
"""
from typing import Dict, List
from datetime import datetime, timedelta
import asyncio
import yaml

from agents.factory import AgentFactory
from agents.ai_agent import AIAgent, ManagerAgent, ExecutiveAgent

# Lazy import circular dependency önlemek için
from systems.meeting import MeetingSystem
from systems.task import TaskManager, TaskPriority
from systems.messaging import MessagingSystem, CollaborationSystem
from systems.goals import GoalManager


class AutonomousCompany:
    """Otonom AI Şirketi - Ana sınıf"""
    
    def __init__(self, config_path: str = "config/company_config.yaml"):
        print("🏢 Otonom AI Şirketi başlatılıyor...\n")
        
        # Config yükle
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.company_name = self.config['company']['name']
        self.vision = self.config['company']['vision']
        self.mission = self.config['company']['mission']
        
        # Sistemleri başlat
        self.agent_factory = AgentFactory(config_path)
        self.agents: Dict[str, AIAgent] = {}
        self.departments: Dict[str, List[AIAgent]] = {}
        
        self.meeting_system = MeetingSystem()
        self.task_manager = TaskManager()
        self.messaging_system = MessagingSystem()
        self.collaboration_system = CollaborationSystem(self.messaging_system)
        self.goal_manager = GoalManager()
        
        self.is_running = False
        self.start_time = None
        
        print(f"✅ {self.company_name} hazır!\n")
    
    async def initialize(self):
        """Şirketi başlat ve ajanları oluştur"""
        print("🚀 Şirket başlatılıyor...\n")
        
        # Ajanları oluştur
        self.agents = self.agent_factory.create_all_agents()
        self.departments = self.agent_factory.departments
        
        # Mesajlaşma sistemine kaydet
        for agent in self.agents.values():
            self.messaging_system.register_agent(agent)
        
        # Departman kanallarını oluştur
        self.messaging_system.create_department_channels(self.departments)
        # Hedefleri config'den yükle
        self.goal_manager.load_goals_from_config(self.config)
        
        
        print(f"\n{'='*60}")
        print(f"🏢 {self.company_name}")
        print(f"{'='*60}")
        print(f"👁️  Vizyon: {self.vision}")
        print(f"🎯 Misyon: {self.mission}")
        print(f"\n📊 Şirket Yapısı:")
        print(f"   • Toplam Çalışan: {len(self.agents)}")
        print(f"   • Departman Sayısı: {len(self.departments)}")
        print(f"   • Yönetici Sayısı: {len(self.agent_factory.get_managers())}")
        print(f"   • Üst Yönetim: {len(self.agent_factory.get_executives())}")
        print(f"{'='*60}\n")
        
        self.is_running = True
        self.start_time = datetime.now()
    
    async def morning_standup(self):
        """Sabah standup toplantıları - Her departman için"""
        print("\n☀️  SABAH STANDUP TOPLANTILARI BAŞLIYOR\n")
        
        for dept_name, dept_agents in self.departments.items():
            if len(dept_agents) > 0:
                # Departman yöneticisini bul
                facilitator = dept_agents[0]  # İlk agent veya manager
                for agent in dept_agents:
                    if isinstance(agent, ManagerAgent):
                        facilitator = agent
                        break
                
                # Toplantı planla ve yürüt
                meeting = await self.meeting_system.schedule_daily_standup(
                    department=dept_name,
                    participants=dept_agents,
                    facilitator=facilitator,
                    scheduled_time=datetime.now()
                )
                
                await self.meeting_system.conduct_daily_standup(
                    meeting=meeting,
                    agents=dept_agents
                )
                
                await asyncio.sleep(2)  # Toplantılar arası bekleme
    
    async def weekly_review(self):
        """Haftalık değerlendirme toplantıları"""
        print("\n📊 HAFTALIK DEĞERLENDİRME TOPLANTILARI\n")
        
        # Departman başları toplantısı
        managers = self.agent_factory.get_managers()
        
        if managers:
            facilitator = managers[0]
            meeting = await self.meeting_system.schedule_weekly_review(
                department="All Departments",
                participants=managers,
                facilitator=facilitator,
                scheduled_time=datetime.now()
            )
            
            await self.meeting_system.conduct_weekly_review(
                meeting=meeting,
                agents=managers
            )
    
    async def monthly_planning(self):
        """Aylık planlama toplantısı"""
        print("\n📈 AYLIK PLANLAMA TOPLANTISI\n")
        
        executives = self.agent_factory.get_executives()
        managers = self.agent_factory.get_managers()
        
        participants = executives + managers[:5]  # Executives + top 5 managers
        
        if participants:
            facilitator = executives[0] if executives else participants[0]
            
            meeting = await self.meeting_system.schedule_monthly_planning(
                participants=participants,
                facilitator=facilitator,
                scheduled_time=datetime.now()
            )
            
            await self.meeting_system.conduct_monthly_planning(
                meeting=meeting,
                agents=participants
            )
    
    async def assign_tasks_to_departments(self):
        """Departmanlara görev dağıt"""
        print("\n📋 GÖREV DAĞITIMI BAŞLIYOR\n")
        
        for dept_name, dept_agents in self.departments.items():
            # Departman yöneticisini bul
            manager = None
            for agent in dept_agents:
                if isinstance(agent, ManagerAgent):
                    manager = agent
                    break
            
            if manager:
                # Yöneticiye görev atama yetkisi ver
                team_members = [a for a in dept_agents if a != manager]
                
                if team_members:
                    await self.task_manager.auto_assign_tasks(
                        manager=manager,
                        available_agents=team_members[:3]  # İlk 3 üye
                    )
    
    async def simulate_work_day(self):
        """Bir iş gününü simüle et"""
        print("\n🌅 YENİ İŞ GÜNÜ BAŞLIYOR\n")
        
        # 1. Sabah standup
        await self.morning_standup()
        
        # 2. Görev dağıtımı
        await self.assign_tasks_to_departments()
        
        # 3. Görevleri çalıştır (simüle)
        print("\n⚙️  ÇALIŞANLAR GÖREVLERİNİ YÜRÜTÜYOR...\n")
        await asyncio.sleep(5)
        
        # 4. Departmanlar arası iş birliği örneği
        tech_agents = self.departments.get('technology', [])
        marketing_agents = self.departments.get('marketing', [])
        
        if tech_agents and marketing_agents:
            await self.collaboration_system.cross_department_meeting(
                departments=['technology', 'marketing'],
                topic="Yeni Ürün Lansmanı Koordinasyonu",
                agents=self.agents
            )
        
        # 5. Günlük rapor
        print(self.task_manager.generate_task_report())
    
    async def run_continuous(self, days: int = 1):
        """Sürekli çalışma modu - Belirtilen gün sayısı kadar"""
        print(f"\n🔄 SÜREKLİ ÇALIŞMA MODU BAŞLATILIYOR ({days} gün)\n")
        
        await self.initialize()
        
        for day in range(days):
            print(f"\n{'='*60}")
            print(f"📅 GÜN {day + 1}")
            print(f"{'='*60}\n")
            
            # Günlük işler
            await self.simulate_work_day()
            
            # Haftalık kontrol (7 günde bir)
            if (day + 1) % 7 == 0:
                await self.weekly_review()
            
            # Aylık kontrol (30 günde bir)
            if (day + 1) % 30 == 0:
                await self.monthly_planning()
            
            # Gece molası simülasyonu
            if day < days - 1:
                print("\n🌙 Gece vardiyası devam ediyor... (7/24 çalışma)\n")
                await asyncio.sleep(3)
    
    async def quick_demo(self):
        """Hızlı demo - Tüm özellikleri göster"""
        print("\n🎬 HIZLI DEMO MODU\n")
        
        await self.initialize()
        
        # 1. Sabah standup (1 departman)
        print("\n1️⃣  Sabah Standup Örneği\n")
        tech_agents = self.departments.get('technology', [])[:5]
        if tech_agents:
            meeting = await self.meeting_system.schedule_daily_standup(
                department="Technology",
                participants=tech_agents,
                facilitator=tech_agents[0],
                scheduled_time=datetime.now()
            )
            await self.meeting_system.conduct_daily_standup(meeting, tech_agents)
        
        await asyncio.sleep(2)
        
        # 2. Görev atama
        print("\n2️⃣  Görev Atama Örneği\n")
        managers = self.agent_factory.get_managers()
        if managers:
            manager = managers[0]
            team = [a for a in self.agents.values() if a.department == manager.department][:3]
            if team:
                await self.task_manager.auto_assign_tasks(manager, team)
        
        await asyncio.sleep(2)
        
        # 3. Departmanlar arası iş birliği
        print("\n3️⃣  Departmanlar Arası İş Birliği\n")
        await self.collaboration_system.cross_department_meeting(
            departments=['technology', 'marketing'],
            topic="AI Ürün Lansmanı",
            agents=self.agents
        )
        
        await asyncio.sleep(2)
        
        # 4. Rapor
        print("\n4️⃣  Görev Raporu\n")
        print(self.task_manager.generate_task_report())
        
        # 5. Şirket özeti
        await self.print_company_status()
    
    async def print_company_status(self):
        """Şirket durumunu yazdır"""
        print(f"\n{'='*60}")
        print(f"📊 ŞİRKET DURUM RAPORU")
        print(f"{'='*60}\n")
        
        print(f"🏢 Şirket: {self.company_name}")
        print(f"⏱️  Çalışma Süresi: {datetime.now() - self.start_time if self.start_time else 'N/A'}")
        print(f"👥 Toplam Çalışan: {len(self.agents)}")
        
        print(f"\n📋 Görev Durumu:")
        stats = self.task_manager.get_task_statistics()
        print(f"   • Toplam: {stats['total_tasks']}")
        print(f"   • Tamamlanan: {stats['completed']}")
        print(f"   • Devam Eden: {stats['in_progress']}")
        print(f"   • Tamamlanma: %{stats['completion_rate']:.1f}")
        
        print(f"\n📅 Toplantılar:")
        print(f"   • Geçmiş Toplantı: {len(self.meeting_system.meeting_history)}")
        print(f"   • Planlanan: {len(self.meeting_system.get_upcoming_meetings())}")
        
        print(f"\n{'='*60}\n")
    
    def get_ceo(self) -> Optional[ExecutiveAgent]:
        """CEO'yu al"""
        for agent in self.agents.values():
            if agent.role == "CEO":
                return agent
        return None
    
    async def shutdown(self):
        """Şirketi kapat"""
        print("\n🛑 Şirket kapatılıyor...")
        self.is_running = False
        
        # Final rapor
        await self.print_company_status()
        
        print("✅ Şirket başarıyla kapatıldı.\n")
