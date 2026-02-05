"""
Show AI Assignments - AI atamalarını göster
"""
from systems.ai_provider import AIProviderManager


def main():
    """AI atama raporunu göster"""
    
    provider_manager = AIProviderManager()
    
    # Detaylı rapor
    print(provider_manager.generate_ai_assignment_report())
    
    # Tier istatistikleri
    stats = provider_manager.get_tier_statistics()
    
    print("\n📊 TIER DAĞILIMI:")
    print(f"   Free/Basic: {stats.get('free', 0) + stats.get('basic', 0)} çalışan")
    print(f"   Pro: {stats.get('pro', 0)} çalışan")
    print(f"   Enterprise: {stats.get('enterprise', 0)} çalışan")
    
    total = sum(stats.values())
    if total > 0:
        print(f"\n💰 MALIYET TAHMİNİ:")
        print(f"   Basic tier (%{stats.get('basic', 0)/total*100:.1f}): ~$50-100/ay")
        print(f"   Pro tier (%{stats.get('pro', 0)/total*100:.1f}): ~$500-1000/ay")
        print(f"   Enterprise tier (%{stats.get('enterprise', 0)/total*100:.1f}): ~$2000-5000/ay")
        print(f"   \nTOPLAM TAHMİNİ: ~$2500-6000/ay")
    
    # Örnek senaryolar
    print("\n\n" + "="*80)
    print("🎯 ÖRNEK GÖREV ATAMALARI")
    print("="*80 + "\n")
    
    example_scenarios = [
        ("Lead Developer", "technology", "Karmaşık mimari tasarım", 9),
        ("Support Agent", "customer_service", "Basit müşteri sorusu", 2),
        ("CEO", "management", "Stratejik karar alma", 10),
        ("Content Creator", "marketing", "Blog yazısı", 5),
        ("Game Developer", "technology", "Yeni oyun mekaniği", 8),
    ]
    
    for role, dept, task, difficulty in example_scenarios:
        result = provider_manager.get_best_ai_for_task(role, dept, task, difficulty)
        
        print(f"👤 {role} - {task}")
        print(f"   🤖 Seçilen AI: {result['selected_ai']}")
        print(f"   📊 Zorluk: {difficulty}/10")
        print(f"   💡 Neden: {result['reason']}")
        print()


if __name__ == "__main__":
    main()
