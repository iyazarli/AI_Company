#!/bin/bash

echo "🚀 Otonom AI Şirket - Hızlı Başlatma"
echo ""

# .env dosyası kontrolü
if [ ! -f .env ]; then
    echo "📝 .env dosyası oluşturuluyor..."
    cp .env.example .env
    echo ""
    echo "⚠️  ÖNEMLİ: .env dosyasını düzenleyin!"
    echo ""
    echo "Aşağıdaki API key'lerden EN AZ BİRİNİ ekleyin:"
    echo ""
    echo "1. OpenAI (Önerilen):"
    echo "   https://platform.openai.com/api-keys"
    echo "   OPENAI_API_KEY=sk-..."
    echo ""
    echo "2. Anthropic (İsteğe bağlı):"
    echo "   https://console.anthropic.com/"
    echo "   ANTHROPIC_API_KEY=sk-ant-..."
    echo ""
    echo "3. Google (İsteğe bağlı):"
    echo "   https://makersuite.google.com/app/apikey"
    echo "   GOOGLE_API_KEY=..."
    echo ""
    echo "Düzenlemek için:"
    echo "  nano .env"
    echo "  veya"
    echo "  code .env"
    echo ""
    read -p "API key ekledikten sonra ENTER'a basın..."
fi

# Sanal ortam kontrolü
if [ ! -d "venv" ]; then
    echo "📦 Sanal ortam oluşturuluyor..."
    python3 -m venv venv
fi

# Aktifleştir
source venv/bin/activate

# Bağımlılıkları kontrol et
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "📥 Bağımlılıklar yükleniyor..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    touch venv/.dependencies_installed
fi

# API key kontrolü
echo ""
echo "🔍 API key'ler kontrol ediliyor..."
python3 -c "
from dotenv import load_dotenv
import os

load_dotenv()

has_key = False
if os.getenv('OPENAI_API_KEY'):
    print('✅ OpenAI API key bulundu')
    has_key = True
if os.getenv('ANTHROPIC_API_KEY'):
    print('✅ Anthropic API key bulundu')
    has_key = True
if os.getenv('GOOGLE_API_KEY'):
    print('✅ Google API key bulundu')
    has_key = True

if not has_key:
    print('')
    print('⚠️  Hiç API key bulunamadı!')
    print('Demo modunda çalışılacak (gerçek AI yanıtları olmayacak)')
    print('')
    print('.env dosyasına en az bir API key ekleyin:')
    print('  OPENAI_API_KEY=sk-...')
    print('')
"

echo ""
echo "🎯 Şirketi başlatmak için:"
echo "  python main.py"
echo ""
echo "📊 Diğer komutlar:"
echo "  python show_ai_assignments.py  - AI atamalarını gör"
echo "  python set_goals.py            - Hedef belirle"
echo "  python dashboard.py            - Dashboard"
echo ""

# Otomatik başlat mı?
read -p "Şimdi başlatmak ister misiniz? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python main.py
fi
