"""
Main Entry Point - Otonom AI Şirketini Başlat
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

from core.company import AutonomousCompany


async def main():
    """Ana program"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       🏢 OTONOM AI ŞİRKET SİMÜLASYONU 🏢                    ║
║                                                              ║
║  Tam otonom çalışan yapay zeka destekli şirket              ║
║  • 8 Departman                                               ║
║  • 50+ AI Çalışan                                            ║
║  • 7/24 Kesintisiz Çalışma                                   ║
║  • Toplantılar, Görevler, İş Birlikleri                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # API key kontrolü
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  UYARI: OPENAI_API_KEY bulunamadı!")
        print("Lütfen .env dosyasını oluşturun ve API anahtarınızı ekleyin.\n")
        print("Örnek:")
        print("  cp .env.example .env")
        print("  # .env dosyasını düzenleyin\n")
        
        demo_mode = input("Demo modunda devam edilsin mi? (y/n): ")
        if demo_mode.lower() != 'y':
            return
    
    # Şirketi oluştur
    company = AutonomousCompany()
    
    print("\nŞirket modunu seçin:")
    print("1. Hızlı Demo (5 dakika)")
    print("2. Tek Gün Simülasyonu")
    print("3. Sürekli Çalışma (7 gün)")
    print("4. Özel Senaryo")
    
    choice = input("\nSeçiminiz (1-4): ").strip()
    
    try:
        if choice == "1":
            # Hızlı demo
            await company.quick_demo()
        
        elif choice == "2":
            # Tek gün
            await company.run_continuous(days=1)
        
        elif choice == "3":
            # 7 gün
            await company.run_continuous(days=7)
        
        elif choice == "4":
            # Özel senaryo
            await custom_scenario(company)
        
        else:
            print("Geçersiz seçim! Hızlı demo başlatılıyor...")
            await company.quick_demo()
        
        # Kapanış
        await company.shutdown()
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Program durduruldu (Ctrl+C)")
        await company.shutdown()
    
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()


async def custom_scenario(company: AutonomousCompany):
    """Özel senaryo - Kullanıcı tanımlı"""
    print("\n🎭 ÖZEL SENARYO MODU\n")
    
    await company.initialize()
    
    print("\nHangi aktiviteyi gerçekleştirmek istersiniz?")
    print("1. Departman Toplantısı")
    print("2. Görev Atama")
    print("3. Departmanlar Arası İş Birliği")
    print("4. Haftalık Review")
    print("5. Aylık Planlama")
    
    activity = input("\nAktivite (1-5): ").strip()
    
    if activity == "1":
        # Departman seç
        print("\nDepartmanlar:")
        for i, dept in enumerate(company.departments.keys(), 1):
            print(f"{i}. {dept}")
        
        dept_choice = input("Departman numarası: ").strip()
        dept_name = list(company.departments.keys())[int(dept_choice) - 1]
        
        agents = company.departments[dept_name][:5]
        meeting = await company.meeting_system.schedule_daily_standup(
            department=dept_name,
            participants=agents,
            facilitator=agents[0],
            scheduled_time=datetime.now()
        )
        await company.meeting_system.conduct_daily_standup(meeting, agents)
    
    elif activity == "2":
        await company.assign_tasks_to_departments()
    
    elif activity == "3":
        await company.collaboration_system.cross_department_meeting(
            departments=['technology', 'marketing', 'business_development'],
            topic="Yeni Strateji Belirleme",
            agents=company.agents
        )
    
    elif activity == "4":
        await company.weekly_review()
    
    elif activity == "5":
        await company.monthly_planning()
    
    await company.print_company_status()


if __name__ == "__main__":
    asyncio.run(main())
