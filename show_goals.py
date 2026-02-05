"""
Show Goals - Mevcut hedefleri göster ve takip et
"""
import asyncio
from dotenv import load_dotenv


import logging
logger = logging.getLogger(__name__)
load_dotenv()

from core.company import AutonomousCompany
from systems.goals import GoalPeriod


async def main():
    """Hedefleri göster"""
    
    company = AutonomousCompany()
    await company.initialize()
    
    # Config'den hedefleri yükle
    company.goal_manager.load_goals_from_config(company.config)
    
    logger.info("\n" + "="*60)
    print("🎯 ŞİRKET HEDEFLERİ")
    logger.info("="*60 + "\n")
    
    logger.info("Ne görmek istersiniz?")
    logger.info("1. Tüm hedefler")
    logger.info("2. Quarterly hedefler")
    logger.info("3. Monthly hedefler")
    logger.info("4. Weekly hedefler")
    logger.info("5. Departman hedefleri")
    logger.info("6. Hedef ilerlemesi güncelle")
    
    choice = input("\nSeçim (1-6): ").strip()
    
    if choice == "1":
        # Tüm hedefler
        print(company.goal_manager.get_goal_report())
    
    elif choice in ["2", "3", "4"]:
        # Periyoda göre
        period_map = {
            "2": GoalPeriod.QUARTERLY,
            "3": GoalPeriod.MONTHLY,
            "4": GoalPeriod.WEEKLY
        }
        period = period_map[choice]
        goals = company.goal_manager.get_active_goals(period)
        
        logger.info(f"\n📅 {period.value.upper()} HEDEFLERİ:\n")
        for i, goal in enumerate(goals, 1):
            logger.info(f"{i}. {goal.title}")
            logger.info(f"   Sorumlu: {goal.owner}")
            logger.info(f"   İlerleme: %{goal.progress:.0f}")
            if goal.deadline:
                logger.info(f"   Son Tarih: {goal.deadline.strftime('%Y-%m-%d')}")
            print()
    
    elif choice == "5":
        # Departman hedefleri
        logger.info("\nDepartman seçin:")
        for i, dept in enumerate(company.departments.keys(), 1):
            logger.info(f"{i}. {dept}")
        
        dept_idx = int(input("\nSeçim: ")) - 1
        dept_name = list(company.departments.keys())[dept_idx]
        
        goals = company.goal_manager.get_department_goals(dept_name)
        
        logger.info(f"\n🏢 {dept_name.upper()} HEDEFLERİ:\n")
        for goal in goals:
            logger.info(f"• {goal.title}")
            logger.info(f"  İlerleme: %{goal.progress:.0f}")
            print()
    
    elif choice == "6":
        # İlerleme güncelle
        all_goals = company.goal_manager.get_active_goals()
        
        logger.info("\nHangi hedefin ilerlemesini güncellemek istersiniz?\n")
        for i, goal in enumerate(all_goals, 1):
            logger.info(f"{i}. {goal.title} (Mevcut: %{goal.progress:.0f})")
        
        goal_idx = int(input("\nSeçim: ")) - 1
        goal = all_goals[goal_idx]
        
        new_progress = float(input(f"\nYeni ilerleme yüzdesi (0-100): "))
        notes = input("Not (opsiyonel): ")
        
        company.goal_manager.update_goal_progress(
            goal.id,
            new_progress,
            notes
        )


if __name__ == "__main__":
    asyncio.run(main())
