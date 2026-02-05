"""
Test AI Assignments - Akıllı dağılımı test et
"""
from systems.auto_config import AutoAIConfigurator



import logging
logger = logging.getLogger(__name__)
def main():
    """AI atamaları test et"""
    
    logger.info("\n" + "="*70)
    print("🧪 AI ATAMA TESTİ - Akıllı Dağılım")
    logger.info("="*70 + "\n")
    
    config = AutoAIConfigurator()
    
    # Test senaryoları
    test_roles = [
        # CODING ROLES (Claude tercih edilmeli)
        ("Backend Developer", 6),
        ("Lead Developer", 9),
        ("iOS Developer", 7),
        ("Game Developer", 8),
        
        # CREATIVE ROLES (GPT tercih edilmeli)
        ("Content Creator", 5),
        ("Marketing Manager", 8),
        ("Social Media Manager", 5),
        
        # RESEARCH/ANALYSIS (Claude tercih edilmeli)
        ("AI Research Scientist", 10),
        ("Data Scientist", 7),
        ("Market Research Analyst", 7),
        
        # EXECUTIVE (Claude Opus tercih edilmeli)
        ("CEO", 10),
        ("CTO", 9),
        
        # SUPPORT (GPT-3.5 ucuz ve hızlı)
        ("Support Agent", 3),
        ("Customer Support", 4),
    ]
    
    logger.info("📋 ROLE BAZLI OPTİMAL AI SEÇİMİ:\n")
    
    for role, difficulty in test_roles:
        model_config = config.get_model_for_role(difficulty, role)
        
        primary = model_config['primary']
        
        # AI provider'ı belirle
        if 'claude' in primary:
            provider_icon = "🔵 Claude"
            strength = "Kod/Analiz"
        elif 'gpt-4' in primary:
            provider_icon = "🟢 GPT-4"
            strength = "Genel/Kreatif"
        elif 'gpt-3.5' in primary:
            provider_icon = "🟡 GPT-3.5"
            strength = "Hızlı/Ucuz"
        else:
            provider_icon = "⚪ Demo"
            strength = "Simülasyon"
        
        logger.info(f"{role:30} → {provider_icon:15} | {primary:35} | {strength}")
    
    logger.info("\n" + "="*70)
    print("✅ Akıllı Dağılım Özeti:")
    logger.info("="*70)
    print("""
🔵 CLAUDE (Coding & Deep Analysis)
   ✓ Tüm yazılım geliştirme rolleri
   ✓ Araştırma ve veri analizi
   ✓ Karmaşık problem çözme
   ✓ Executive stratejik kararlar

🟢 GPT-4 (Creative & General)
   ✓ Marketing ve içerik üretimi
   ✓ Yaratıcı yazım
   ✓ Müşteri iletişimi
   ✓ Genel iş görevleri

🟡 GPT-3.5 (Fast & Economical)
   ✓ Müşteri desteği
   ✓ Basit görevler
   ✓ Hızlı yanıtlar

💡 Her AI'ın güçlü yönü kullanılıyor!
    """)


if __name__ == "__main__":
    main()
