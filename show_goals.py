"""
Show Goals - Mevcut hedefleri göster ve takip et
"""
import asyncio
from dotenv import load_dotenv

load_dotenv()

from core.company import AutonomousCompany
from systems.goals import GoalPeriod


async def main():
    """Hedefleri göster"""
    
    company = AutonomousCompany()
    await company.initialize()
    
    # Config'den hedefleri yükle
    company.goal_manager.load_goals_from_config(company.config)
    
    print("\n" + "="*60)
    print("🎯 ŞİRKET HEDEFLERİ")
    print("="*60 + "\n")
    
    print("Ne görmek istersiniz?")
    print("1. Tüm hedefler")
    print("2. Quarterly hedefler")
    print("3. Monthly hedefler")
    print("4. Weekly hedefler")
    print("5. Departman hedefleri")
    print("6. Hedef ilerlemesi güncelle")
    
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
        
        print(f"\n📅 {period.value.upper()} HEDEFLERİ:\n")
        for i, goal in enumerate(goals, 1):
            print(f"{i}. {goal.title}")
            print(f"   Sorumlu: {goal.owner}")
            print(f"   İlerleme: %{goal.progress:.0f}")
            if goal.deadline:
                print(f"   Son Tarih: {goal.deadline.strftime('%Y-%m-%d')}")
            print()
    
    elif choice == "5":
        # Departman hedefleri
        print("\nDepartman seçin:")
        for i, dept in enumerate(company.departments.keys(), 1):
            print(f"{i}. {dept}")
        
        dept_idx = int(input("\nSeçim: ")) - 1
        dept_name = list(company.departments.keys())[dept_idx]
        
        goals = company.goal_manager.get_department_goals(dept_name)
        
        print(f"\n🏢 {dept_name.upper()} HEDEFLERİ:\n")
        for goal in goals:
            print(f"• {goal.title}")
            print(f"  İlerleme: %{goal.progress:.0f}")
            print()
    
    elif choice == "6":
        # İlerleme güncelle
        all_goals = company.goal_manager.get_active_goals()
        
        print("\nHangi hedefin ilerlemesini güncellemek istersiniz?\n")
        for i, goal in enumerate(all_goals, 1):
            print(f"{i}. {goal.title} (Mevcut: %{goal.progress:.0f})")
        
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
