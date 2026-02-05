"""
Set Company Goals - Şirket hedeflerini belirle
"""
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv


import logging
logger = logging.getLogger(__name__)
load_dotenv()

from core.company import AutonomousCompany
from systems.goals import GoalManager, GoalSettingInterface, GoalPeriod


async def main():
    """Hedef belirleme arayüzü"""
    
    logger.info("""
╔══════════════════════════════════════════════════════════════╗
║          🎯 ŞİRKET HEDEFLERİNİ BELİRLE 🎯                   ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Şirketi başlat
    company = AutonomousCompany()
    await company.initialize()
    
    logger.info("\nHedef belirleme yöntemi seçin:")
    logger.info("1. İnteraktif (Tek tek hedef gir)")
    logger.info("2. Hızlı (Hazır şablon)")
    logger.info("3. Config'den yükle")
    logger.info("4. Departman hedefleri")
    
    choice = input("\nSeçim (1-4): ").strip()
    
    goal_interface = GoalSettingInterface(company.goal_manager)
    
    if choice == "1":
        # İnteraktif mod
        logger.info("\nKaç hedef belirlemek istiyorsunuz?")
        num_goals = int(input("Sayı: ") or "1")
        
        for i in range(num_goals):
            logger.info(f"\n--- Hedef {i+1}/{num_goals} ---")
            goal_interface.interactive_goal_setting()
    
    elif choice == "2":
        # Hızlı şablon
        template_goals = [
            {
                "title": "3 Yeni Mobil Uygulama Lansmanı",
                "description": "Q1 2026'da 3 yeni mobil uygulama piyasaya sür",
                "period": "quarterly",
                "owner": "CTO"
            },
            {
                "title": "2 Oyun Projesi Tamamlama",
                "description": "Unity ve Unreal ile 2 oyun projesi bitir",
                "period": "quarterly",
                "owner": "Technology/game_development"
            },
            {
                "title": "%30 Gelir Artışı",
                "description": "Bir önceki çeyreğe göre %30 gelir artışı",
                "period": "quarterly",
                "owner": "CFO"
            },
            {
                "title": "AI Ürün Portföyü Genişletme",
                "description": "5 yeni AI/ML ürün geliştir",
                "period": "quarterly",
                "owner": "Technology/ai_ml"
            },
            {
                "title": "Müşteri Memnuniyeti %95+",
                "description": "Müşteri memnuniyetini %95'in üzerinde tut",
                "period": "monthly",
                "owner": "Customer Service"
            }
        ]
        
        goal_interface.quick_set_goals(template_goals)
    
    elif choice == "3":
        # Config'den yükle
        logger.info("\nConfig'den hedefler yükleniyor...")
        company.goal_manager.load_goals_from_config(company.config)
    
    elif choice == "4":
        # Departman hedefleri
        logger.info("\nDepartmanlar:")
        for i, dept in enumerate(company.departments.keys(), 1):
            logger.info(f"{i}. {dept}")
        
        dept_idx = int(input("\nDepartman seçin: ")) - 1
        dept_name = list(company.departments.keys())[dept_idx]
        
        title = input("Hedef: ")
        description = input("Açıklama: ")
        
        # Departman yöneticisini bul
        dept_agents = company.departments[dept_name]
        owner = dept_agents[0].name if dept_agents else "Manager"
        
        company.goal_manager.set_department_goal(
            department=dept_name,
            title=title,
            description=description,
            period=GoalPeriod.MONTHLY,
            owner=owner
        )
    
    # Raporu göster
    print(company.goal_manager.get_goal_report())
    
    # CEO'ya hedefleri sun
    ceo = company.get_ceo()
    if ceo:
        logger.info("\n" + "="*60)
        print("💼 CEO'ya hedefler sunuluyor...")
        logger.info("="*60 + "\n")
        
        active_goals = company.goal_manager.get_active_goals()
        goal_summary = "\n".join([
            f"- {g.title} ({g.period.value}, Sorumlu: {g.owner})"
            for g in active_goals[:5]
        ])
        
        # CEO'nun hedefler hakkında görüşünü al
        decision = await ceo.make_strategic_decision(
            f"""Şirket için belirlenen hedefler:

{goal_summary}

Bu hedefleri değerlendir:
1. Hedefler şirket vizyonu ile uyumlu mu?
2. Gerçekçi mi?
3. Önceliklendirme önerilerin neler?
4. Ek hedef önerilerin var mı?
"""
        )
        
        logger.info(f"\n💬 {ceo.name} (CEO):")
        print(decision['decision'])
    
    logger.info("\n✅ Hedef belirleme tamamlandı!")
    logger.info("\nHedefleri görmek için:")
    logger.info("  python show_goals.py")
    logger.info("\nŞirketi hedeflerle başlatmak için:")
    logger.info("  python main.py")


if __name__ == "__main__":
    asyncio.run(main())
