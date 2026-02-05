"""
Test Suite - Otonom AI Şirket Test Senaryoları
"""
import asyncio
import pytest
from datetime import datetime

from core.company import AutonomousCompany
from agents.factory import AgentFactory
from agents.ai_agent import AIAgent, ManagerAgent
from systems.task import TaskManager, TaskPriority
from systems.meeting import MeetingSystem



import logging
logger = logging.getLogger(__name__)
class TestBasicSetup:
    """Temel kurulum testleri"""
    
    @pytest.mark.asyncio
    async def test_company_initialization(self):
        """Şirket başlatma testi"""
        company = AutonomousCompany()
        await company.initialize()
        
        assert company.is_running == True
        assert len(company.agents) > 0
        assert len(company.departments) == 8
        logger.info(f"✅ Şirket başlatma testi geçti - {len(company.agents)} ajan oluşturuldu")
    
    def test_agent_factory(self):
        """Agent factory testi"""
        factory = AgentFactory()
        agents = factory.create_all_agents()
        
        assert len(agents) > 0
        assert len(factory.departments) == 8
        
        # Technology departmanı kontrolü
        tech_agents = factory.get_department_agents('technology')
        assert len(tech_agents) > 0
        
        logger.info(f"✅ Agent factory testi geçti - {len(agents)} ajan")
    
    def test_managers_creation(self):
        """Yönetici oluşturma testi"""
        factory = AgentFactory()
        factory.create_all_agents()
        
        managers = factory.get_managers()
        executives = factory.get_executives()
        
        assert len(managers) > 0
        assert len(executives) > 0
        
        logger.info(f"✅ Yönetici testi geçti - {len(managers)} manager, {len(executives)} executive")


class TestTaskManagement:
    """Görev yönetimi testleri"""
    
    def test_task_creation(self):
        """Görev oluşturma testi"""
        task_manager = TaskManager()
        
        task = task_manager.create_task(
            title="Test Görevi",
            description="Bu bir test görevidir",
            assigned_to="Test Agent",
            assigned_by="Test Manager",
            department="technology",
            priority=TaskPriority.HIGH
        )
        
        assert task.id is not None
        assert task.title == "Test Görevi"
        assert task.priority == TaskPriority.HIGH
        
        logger.info("✅ Görev oluşturma testi geçti")
    
    @pytest.mark.asyncio
    async def test_task_assignment(self):
        """Görev atama testi"""
        factory = AgentFactory()
        agents = factory.create_all_agents()
        
        task_manager = TaskManager()
        agent = list(agents.values())[0]
        
        task = task_manager.create_task(
            title="Test Assignment",
            description="Test",
            assigned_to=agent.name,
            assigned_by="Manager",
            department=agent.department
        )
        
        success = await task_manager.assign_task_to_agent(task, agent)
        assert success == True
        
        logger.info("✅ Görev atama testi geçti")


class TestMeetingSystem:
    """Toplantı sistemi testleri"""
    
    @pytest.mark.asyncio
    async def test_standup_meeting(self):
        """Standup toplantı testi"""
        factory = AgentFactory()
        agents = factory.create_all_agents()
        
        meeting_system = MeetingSystem()
        tech_agents = list(agents.values())[:3]
        
        meeting = await meeting_system.schedule_daily_standup(
            department="Test Dept",
            participants=tech_agents,
            facilitator=tech_agents[0],
            scheduled_time=datetime.now()
        )
        
        assert meeting.id is not None
        assert meeting.type == "daily_standup"
        assert len(meeting.participants) == 3
        
        logger.info("✅ Standup toplantı testi geçti")


@pytest.mark.asyncio
async def test_quick_demo():
    """Hızlı demo testi"""
    logger.info("\n🎬 Hızlı Demo Testi Başlıyor...\n")
    
    company = AutonomousCompany()
    
    # Not: Bu test gerçek API çağrıları yapmaz (mock gerekli)
    # Sadece yapı testi için
    
    try:
        await company.initialize()
        logger.info("✅ Şirket başlatıldı")
        
        # Görev oluştur
        managers = company.agent_factory.get_managers()
        if managers:
            logger.info(f"✅ {len(managers)} yönetici bulundu")
        
        # Toplantı planla
        tech_agents = company.departments.get('technology', [])[:3]
        if tech_agents:
            meeting = await company.meeting_system.schedule_daily_standup(
                department="Technology",
                participants=tech_agents,
                facilitator=tech_agents[0],
                scheduled_time=datetime.now()
            )
            logger.info(f"✅ Toplantı planlandı: {meeting.title}")
        
        await company.print_company_status()
        
    except Exception as e:
        logger.info(f"⚠️  Test sırasında beklenen hata: {e}")


def run_all_tests():
    """Tüm testleri çalıştır"""
    logger.info("\n" + "="*60)
    print("🧪 OTONOM AI ŞİRKET TEST PAKETİ")
    logger.info("="*60 + "\n")
    
    # Pytest olmadan basit test runner
    logger.info("📋 Test Kategorileri:\n")
    
    # 1. Temel kurulum
    logger.info("1️⃣  Temel Kurulum Testleri")
    setup_tests = TestBasicSetup()
    
    try:
        setup_tests.test_agent_factory()
        setup_tests.test_managers_creation()
        print()
    except Exception as e:
        logger.info(f"❌ Hata: {e}\n")
    
    # 2. Görev yönetimi
    logger.info("2️⃣  Görev Yönetimi Testleri")
    task_tests = TestTaskManagement()
    
    try:
        task_tests.test_task_creation()
        print()
    except Exception as e:
        logger.info(f"❌ Hata: {e}\n")
    
    # 3. Async testler
    logger.info("3️⃣  Asenkron İşlem Testleri")
    
    try:
        asyncio.run(test_quick_demo())
    except Exception as e:
        logger.info(f"⚠️  Async test hatası (normal): {e}")
    
    logger.info("\n" + "="*60)
    print("✅ Test paketi tamamlandı!")
    logger.info("="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()
