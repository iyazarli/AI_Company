#!/bin/bash

# 🌐 Web Dashboard Başlatma Script'i
# Streamlit Dashboard ve FastAPI Backend'i başlatır

set -e

echo "🌐 Otonom AI Şirketi - Web Dashboard Başlatılıyor..."
echo "=================================================="

# Renk kodları
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 bulunamadı! Lütfen Python 3.8+ yükleyin.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python bulundu${NC}"

# Virtual environment kontrolü (opsiyonel)
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment bulunamadı${NC}"
    echo "Virtual environment oluşturmak ister misiniz? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}📦 Virtual environment oluşturuluyor...${NC}"
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment oluşturuldu${NC}"
    fi
fi

# Virtual environment aktif et (varsa)
if [ -d "venv" ]; then
    echo -e "${BLUE}🔧 Virtual environment aktif ediliyor...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment aktif${NC}"
fi

# Paket kontrolü ve kurulum
echo -e "${BLUE}📦 Paketler kontrol ediliyor...${NC}"

if ! python3 -c "import streamlit" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Streamlit yüklü değil, yükleniyor...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Tüm paketler yüklendi${NC}"
else
    echo -e "${GREEN}✓ Paketler hazır${NC}"
fi

# .env dosyası kontrolü
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env dosyası bulunamadı${NC}"
    echo -e "${BLUE}📝 .env dosyası oluşturuluyor...${NC}"
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ .env dosyası oluşturuldu${NC}"
    else
        echo "OPENAI_API_KEY=your-openai-api-key" > .env
        echo "ANTHROPIC_API_KEY=your-anthropic-api-key" >> .env
        echo "GOOGLE_API_KEY=your-google-api-key" >> .env
        echo -e "${GREEN}✓ .env dosyası oluşturuldu${NC}"
    fi
    
    echo -e "${YELLOW}⚠️  Lütfen .env dosyasına API anahtarlarınızı ekleyin!${NC}"
fi

echo ""
echo "=================================================="
echo -e "${GREEN}🚀 Web Dashboard Başlatılıyor...${NC}"
echo "=================================================="
echo ""

# Port kontrolü
API_PORT=8000
STREAMLIT_PORT=8501

echo -e "${BLUE}📡 API Backend başlatılıyor (Port: $API_PORT)...${NC}"

# API'yi arka planda başlat
python3 -m uvicorn api.main:app --host 0.0.0.0 --port $API_PORT --reload &
API_PID=$!

echo -e "${GREEN}✓ API Backend başlatıldı (PID: $API_PID)${NC}"

# API'nin hazır olmasını bekle
echo -e "${BLUE}⏳ API hazırlanıyor...${NC}"
sleep 3

# API health check
for i in {1..10}; do
    if curl -s http://localhost:$API_PORT/health > /dev/null; then
        echo -e "${GREEN}✓ API hazır!${NC}"
        break
    fi
    echo -e "${YELLOW}⏳ Bekleniyor... ($i/10)${NC}"
    sleep 1
done

echo ""
echo -e "${BLUE}🎨 Streamlit Dashboard başlatılıyor (Port: $STREAMLIT_PORT)...${NC}"

# Streamlit'i başlat
streamlit run dashboard/streamlit_app.py --server.port $STREAMLIT_PORT --server.headless false &
STREAMLIT_PID=$!

echo -e "${GREEN}✓ Streamlit Dashboard başlatıldı (PID: $STREAMLIT_PID)${NC}"

echo ""
echo "=================================================="
echo -e "${GREEN}✅ Web Dashboard Hazır!${NC}"
echo "=================================================="
echo ""
echo -e "${BLUE}📊 Streamlit Dashboard:${NC} http://localhost:$STREAMLIT_PORT"
echo -e "${BLUE}🌐 FastAPI Backend:${NC}     http://localhost:$API_PORT"
echo -e "${BLUE}📚 API Docs:${NC}            http://localhost:$API_PORT/docs"
echo ""
echo -e "${YELLOW}⚡ Durdurmak için: Ctrl+C${NC}"
echo ""

# Cleanup fonksiyonu
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Kapatılıyor...${NC}"
    
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null || true
        echo -e "${GREEN}✓ API Backend kapatıldı${NC}"
    fi
    
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill $STREAMLIT_PID 2>/dev/null || true
        echo -e "${GREEN}✓ Streamlit Dashboard kapatıldı${NC}"
    fi
    
    echo -e "${GREEN}✅ Temizleme tamamlandı${NC}"
    exit 0
}

# Ctrl+C yakalandığında cleanup çalıştır
trap cleanup INT TERM

# İki process'i de bekle
wait
