# 🏢 Otonom AI Şirket Simülasyonu

Tam otonom çalışan bir yapay zeka şirketi simülasyonu. 8 departman, 50+ AI çalışan ajanı ile 7/24 kesintisiz çalışır.

## 🚀 Hızlı Başlangıç

### 🌐 Web Dashboard (Önerilen - Streamlit + FastAPI)

```bash
./start_web.sh     # Linux/Mac
# veya
start_web.bat      # Windows
```

**Otomatik açılır:**
- 📊 **Dashboard:** http://localhost:8501
- 🌐 **API:** http://localhost:8000/docs

### 💻 Terminal Modu

```bash
./quick_start.sh   # Linux/Mac
# veya
quick_start.bat    # Windows
```

---

## 📊 Departman Yapısı

### 1. Yazılım/Teknoloji Departmanı
- **Web Development Team**: Lead Dev, Backend, Frontend, Full Stack, UI/UX Designer
- **Mobile Development Team**: iOS, Android, React Native/Flutter, Mobile UI/UX
- **Game Development Team**: Game Developer, Designer, Character Artist, 3D Modeler, Animator, Level Designer, Game Tester
- **AI/ML Team**: AI/ML Engineer, Research Scientist, NLP Specialist, Computer Vision, Prompt Engineer, Data Scientist, MLOps
- **Infrastructure**: DevOps, QA, DBA, Security, Technical Writer

### 2. Marketing Departmanı
Marketing Manager, Content Creator, Social Media Manager, SEO Specialist, Graphic Designer

### 3. İş Geliştirme Departmanı
Business Development Manager, Sales Rep, Partnership Manager, Market Research Analyst

### 4. Finans & Muhasebe
CFO, Accountant, Budget Analyst

### 5. İnsan Kaynakları
HR Manager, Recruiter, Employee Relations Specialist

### 6. Müşteri Hizmetleri
Customer Support Manager, Support Agent, Account Manager

### 7. Yönetim & Koordinasyon
CEO, Project Manager, Operations Manager

### 8. Hukuk & Uyumluluk
Legal Advisor, Compliance Officer

## 🚀 Özellikler

- ✅ **Otomatik AI Konfigürasyonu** - API key'e göre optimal dağılım
- ✅ 50+ AI çalışan ajanı (GPT-4, Claude, Gemini destekli)
- ✅ Zorluk seviyesine göre akıllı AI ataması
- ✅ Günlük standup, haftalık review, aylık planlama toplantıları
- ✅ Otomatik görev atama ve takip
- ✅ Departmanlar arası iletişim ve koordinasyon
- ✅ 7/24 kesintisiz çalışma döngüsü
- ✅ Dinamik hedef belirleme sistemi
- ✅ Performans metrikleri ve raporlama
- ✅ Hiyerarşik yönetim yapısı
- ✅ Otonom karar alma mekanizmaları

## 🛠️ Kurulum

### Hızlı Başlatma (Önerilen)

```bash
# Tek komutla başlat
chmod +x quick_start.sh
./quick_start.sh

# Windows için
quick_start.bat
```

### Manuel Kurulum

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. API anahtarını ekle
cp .env.example .env
nano .env  # En az bir API key ekle

# 3. Başlat
python main.py
```

### API Anahtarları

**Sadece EN AZ BİR tane eklemeniz yeterli:**

1. **OpenAI** (Önerilen): https://platform.openai.com/api-keys
   ```
   OPENAI_API_KEY=sk-...
   ```

2. **Anthropic** (İsteğe bağlı): https://console.anthropic.com/
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Google** (İsteğe bağlı): https://makersuite.google.com/app/apikey
   ```
   GOOGLE_API_KEY=...
   ```

> 💡 Sistem otomatik olarak mevcut API key'lere göre en iyi AI dağılımını yapacak!

## 🎮 Kullanım

```bash
# Şirketi başlat
python main.py

# Belirli bir departmanı başlat
python main.py --department software

# Toplantı simülasyonu
python run_meeting.py --type daily-standup

# Görev dashboard
python dashboard.py
```

## 📁 Proje Yapısı

```
autonomous-ai-company/
├── agents/              # AI agent tanımları
│   ├── base_agent.py
│   ├── departments/     # Departman ajanları
│   ├── roles/          # Rol bazlı ajanlar
│   └── managers/       # Yönetici ajanları
├── systems/            # Alt sistemler
│   ├── meeting.py      # Toplantı sistemi
│   ├── task.py         # Görev yönetimi
│   ├── messaging.py    # İletişim sistemi
│   └── reporting.py    # Raporlama
├── core/               # Çekirdek sistemler
│   ├── company.py      # Şirket ana sınıfı
│   ├── department.py   # Departman yönetimi
│   └── scheduler.py    # Zamanlama motoru
├── config/             # Konfigürasyon
├── data/               # Veri ve loglar
├── main.py             # Ana başlatıcı
└── dashboard.py        # İzleme dashboard
```

## 🔄 Çalışma Döngüsü

1. **Başlangıç**: Tüm ajanlar aktive olur
2. **Sabah Toplantısı**: Her departman günlük standup yapar
3. **Görev Dağılımı**: Yöneticiler görevleri dağıtır
4. **Çalışma**: Ajanlar görevlerini execute eder
5. **İletişim**: Departmanlar arası koordinasyon
6. **Raporlama**: Günlük, haftalık, aylık raporlar
7. **Döngü**: 7/24 sürekli tekrar

## 📊 İzleme

Dashboard üzerinden:
- Aktif görevler
- Departman performansı
- Tamamlanan işler
- Toplantı kayıtları
- Çalışan metrikleri

## 🔧 Yapılandırma

`config/company_config.yaml` dosyasından şirket hedeflerini, departman yapısını ve çalışma parametrelerini özelleştirebilirsiniz.
