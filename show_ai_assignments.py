"""
Show AI Assignments - AI atamalarını göster
"""
from systems.ai_provider import AIProviderManager



import logging
logger = logging.getLogger(__name__)
def main():
    """AI atama raporunu göster"""
    
    provider_manager = AIProviderManager()
    
    # Detaylı rapor
    print(provider_manager.generate_ai_assignment_report())
    
    # Tier istatistikleri
    stats = provider_manager.get_tier_statistics()
    
    logger.info("\n📊 TIER DAĞILIMI:")
    logger.info(f"   Free/Basic: {stats.get('free', 0) + stats.get('basic', 0)} çalışan")
    logger.info(f"   Pro: {stats.get('pro', 0)} çalışan")
    logger.info(f"   Enterprise: {stats.get('enterprise', 0)} çalışan")
    
    total = sum(stats.values())
    if total > 0:
        logger.info(f"\n💰 MALIYET TAHMİNİ:")
        logger.info(f"   Basic tier (%{stats.get('basic', 0)/total*100:.1f}): ~$50-100/ay")
        logger.info(f"   Pro tier (%{stats.get('pro', 0)/total*100:.1f}): ~$500-1000/ay")
        logger.info(f"   Enterprise tier (%{stats.get('enterprise', 0)/total*100:.1f}): ~$2000-5000/ay")
        logger.info(f"   \nTOPLAM TAHMİNİ: ~$2500-6000/ay")
    
    # Örnek senaryolar
    logger.info("\n\n" + "="*80)
    print("🎯 ÖRNEK GÖREV ATAMALARI")
    logger.info("="*80 + "\n")
    
    example_scenarios = [
        ("Lead Developer", "technology", "Karmaşık mimari tasarım", 9),
        ("Support Agent", "customer_service", "Basit müşteri sorusu", 2),
        ("CEO", "management", "Stratejik karar alma", 10),
        ("Content Creator", "marketing", "Blog yazısı", 5),
        ("Game Developer", "technology", "Yeni oyun mekaniği", 8),
    ]
    
    for role, dept, task, difficulty in example_scenarios:
        result = provider_manager.get_best_ai_for_task(role, dept, task, difficulty)
        
        logger.info(f"👤 {role} - {task}")
        logger.info(f"   🤖 Seçilen AI: {result['selected_ai']}")
        logger.info(f"   📊 Zorluk: {difficulty}/10")
        logger.info(f"   💡 Neden: {result['reason']}")
        print()


if __name__ == "__main__":
    main()
