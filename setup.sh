#!/bin/bash

# Otonom AI Şirket - Kurulum Scripti

echo "🏢 Otonom AI Şirket Kurulumu Başlıyor..."
echo ""

# Python versiyonu kontrolü
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 bulunamadı! Lütfen Python 3.8+ yükleyin."
    exit 1
fi

echo "✅ Python bulundu: $(python3 --version)"
echo ""

# Sanal ortam oluştur
echo "📦 Sanal ortam oluşturuluyor..."
python3 -m venv venv

# Sanal ortamı aktifleştir
echo "🔌 Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# Bağımlılıkları yükle
echo "📥 Bağımlılıklar yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt

# .env dosyası oluştur
if [ ! -f .env ]; then
    echo "📝 .env dosyası oluşturuluyor..."
    cp .env.example .env
    echo ""
    echo "⚠️  ÖNEMLI: .env dosyasını düzenleyin ve API anahtarlarınızı ekleyin!"
    echo "   - OPENAI_API_KEY"
    echo "   - ANTHROPIC_API_KEY (opsiyonel)"
fi

# Data klasörlerini oluştur
echo "📁 Data klasörleri oluşturuluyor..."
mkdir -p data/logs
mkdir -p data/tasks
mkdir -p data/meetings
mkdir -p data/reports

echo ""
echo "✅ Kurulum tamamlandı!"
echo ""
echo "🚀 Başlatmak için:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "📊 Dashboard için:"
echo "   python dashboard.py"
echo ""
echo "🎤 Toplantı simülasyonu için:"
echo "   python run_meeting.py --type daily-standup"
echo ""
