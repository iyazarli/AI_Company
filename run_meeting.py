"""
Run Meeting - Toplantı simülasyonları
"""
import asyncio
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from core.company import AutonomousCompany


async def main():
    """Toplantı simülasyonu çalıştır"""
    
    if len(sys.argv) < 2:
        print("Kullanım: python run_meeting.py --type <meeting_type>")
        print("\nToplantı Türleri:")
        print("  daily-standup    - Günlük standup")
        print("  weekly-review    - Haftalık değerlendirme")
        print("  monthly-planning - Aylık planlama")
        print("  cross-dept       - Departmanlar arası")
        return
    
    meeting_type = sys.argv[2] if len(sys.argv) > 2 else "daily-standup"
    
    print(f"\n🎤 Toplantı Simülasyonu: {meeting_type}\n")
    
    # Şirketi başlat
    company = AutonomousCompany()
    await company.initialize()
    
    # Toplantı türüne göre çalıştır
    if meeting_type == "daily-standup":
        # Her departman için standup
        for dept_name, agents in company.departments.items():
            if agents:
                print(f"\n{'='*60}")
                print(f"📍 Departman: {dept_name}")
                print(f"{'='*60}\n")
                
                facilitator = agents[0]
                meeting = await company.meeting_system.schedule_daily_standup(
                    department=dept_name,
                    participants=agents[:5],  # İlk 5 kişi
                    facilitator=facilitator,
                    scheduled_time=datetime.now()
                )
                
                await company.meeting_system.conduct_daily_standup(
                    meeting=meeting,
                    agents=agents[:5]
                )
                
                await asyncio.sleep(1)
    
    elif meeting_type == "weekly-review":
        await company.weekly_review()
    
    elif meeting_type == "monthly-planning":
        await company.monthly_planning()
    
    elif meeting_type == "cross-dept":
        await company.collaboration_system.cross_department_meeting(
            departments=['technology', 'marketing', 'business_development'],
            topic="Q1 2026 Strateji Toplantısı",
            agents=company.agents
        )
    
    print("\n✅ Toplantı tamamlandı!\n")


if __name__ == "__main__":
    asyncio.run(main())
