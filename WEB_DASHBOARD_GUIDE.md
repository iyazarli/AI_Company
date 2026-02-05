# 🌐 Web Dashboard Kullanım Kılavuzu

## 🚀 Hızlı Başlangıç

### Tek Komutla Başlatma

**macOS/Linux:**
```bash
./start_web.sh
```

**Windows:**
```bash
start_web.bat
```

Bu komut otomatik olarak:
- ✅ Gerekli paketleri kontrol eder
- ✅ API Backend'i başlatır (Port 8000)
- ✅ Streamlit Dashboard'u başlatır (Port 8501)
- ✅ Tarayıcıda otomatik açar

---

## 📊 Dashboard Özellikleri

### 1️⃣ Ana Dashboard (streamlit_app.py)

**Erişim:** http://localhost:8501

#### Özellikler:
- 📊 **Genel Bakış:** Şirket durumu, çalışan sayısı, hedefler
- 👥 **Çalışanlar:** Tüm AI çalışanların listesi, filtreleme, arama
- 📋 **Görevler:** Görev yönetimi ve durum takibi
- 🎯 **Hedefler:** Şirket hedefleri ve ilerleme
- 💬 **Toplantılar:** Toplantı kayıtları ve notları
- 📈 **İstatistikler:** Detaylı grafikler ve analizler
- 🔧 **Ayarlar:** API key yapılandırması

#### 7 Ana Tab:
1. **Genel Bakış** - Şirket özeti ve metrikler
2. **Çalışanlar** - 50+ AI çalışanın detayları
3. **Görevler** - Görev listesi ve durumları
4. **Hedefler** - Hedef yönetimi ve takibi
5. **Toplantılar** - Toplantı geçmişi
6. **İstatistikler** - Grafikler ve raporlar
7. **Ayarlar** - Sistem konfigürasyonu

---

### 2️⃣ Live Monitor (pages/1_Live_Monitor.py)

**Erişim:** Sidebar → "Live Monitor" sekmesi

#### Özellikler:
- 🔴 **Real-time İzleme:** Canlı aktivite akışı
- 📊 **Görev Akışı:** Güncel görev durumu
- 🎯 **Hedef Takibi:** Hedef ilerleme grafiği
- 🤖 **AI Dağılımı:** Hangi AI hangi role atandı
- 🔄 **Otomatik Yenileme:** 1-30 saniye aralıklarla
- ⚡ **Hızlı Aksiyonlar:** Toplantı, simülasyon başlatma

---

### 3️⃣ Control Panel (pages/2_Control_Panel.py)

**Erişim:** Sidebar → "Control Panel" sekmesi

#### 4 Ana Bölüm:

##### 🎯 Hedef Ekle
- Başlık, açıklama, departman seçimi
- Öncelik seviyesi (1-10)
- Ölçülebilir metrikler
- Hedef tarih belirleme

##### 📋 Görev Oluştur
- Görev başlık ve detay
- Öncelik seviyesi
- Çalışan seçimi (otomatik veya manuel)
- Anlık atama

##### 💬 Mesaj Gönder
- Çalışanlar arası mesajlaşma
- Toplu mesaj gönderme
- *(Yakında aktif olacak)*

##### ⚙️ Şirket Kontrolü
- Şirket başlat/durdur
- API key yapılandırması
- Sistem bilgileri

---

## 🌐 FastAPI Backend

**Erişim:** http://localhost:8000

### API Endpoints

#### Genel
- `GET /` - API ana sayfa
- `GET /health` - Sistem sağlık kontrolü
- `GET /api/status` - Şirket durumu

#### Şirket Yönetimi
- `POST /api/start` - Şirketi başlat
- `POST /api/stop` - Şirketi durdur
- `POST /api/configure` - API key yapılandır

#### Çalışanlar
- `GET /api/agents` - Tüm çalışanlar
- `GET /api/agents/{name}` - Çalışan detayı
- `GET /api/departments` - Departmanlar

#### Görevler
- `GET /api/tasks` - Tüm görevler
- `POST /api/tasks` - Yeni görev oluştur
- `GET /api/tasks?status=pending` - Filtreli görevler

#### Hedefler
- `GET /api/goals` - Tüm hedefler
- `POST /api/goals` - Yeni hedef ekle

#### Toplantılar
- `GET /api/meetings` - Toplantı kayıtları
- `POST /api/meetings/standup` - Standup toplantısı başlat

#### Simülasyon
- `POST /api/simulate/day` - Bir iş günü simüle et

#### İstatistikler
- `GET /api/stats` - Detaylı istatistikler

#### WebSocket
- `WS /ws` - Real-time güncellemeler

### 📚 API Dokümantasyonu

**Swagger UI:** http://localhost:8000/docs
**ReDoc:** http://localhost:8000/redoc

---

## 🔧 Manuel Başlatma

### 1. API Backend'i Başlat

```bash
cd /tmp/workspace
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Streamlit Dashboard'u Başlat

```bash
cd /tmp/workspace
streamlit run dashboard/streamlit_app.py --server.port 8501
```

---

## 🎨 Kullanım Örnekleri

### Örnek 1: Şirketi Başlat ve Hedef Ekle

1. `./start_web.sh` ile web dashboard'u başlat
2. Tarayıcıda http://localhost:8501 aç
3. Sidebar'dan "Şirketi Başlat" butonuna tıkla
4. "Control Panel" sekmesine git
5. "Hedef Ekle" bölümünden yeni hedef oluştur
6. "Live Monitor" sekmesinden ilerlemeyi izle

### Örnek 2: Görev Oluştur ve Takip Et

1. "Control Panel" → "Görev Oluştur"
2. Görev başlığı: "API endpoint geliştir"
3. Çalışan seç veya otomatik ata
4. "Ana Dashboard" → "Görevler" sekmesinden görev durumunu izle

### Örnek 3: Günlük Toplantı Yap

1. Sidebar → "Hızlı Aksiyonlar"
2. "📊 Günlük Toplantı" butonuna tıkla
3. "Toplantılar" sekmesinden toplantı notlarını gör

---

## 🔐 API Key Yapılandırma

### Yöntem 1: Streamlit UI Üzerinden

1. "Ayarlar" sekmesine git
2. API anahtarlarını gir
3. "Kaydet" butonuna tıkla
4. Şirketi yeniden başlat

### Yöntem 2: .env Dosyası

`.env` dosyasını düzenle:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
```

---

## 📊 Real-Time Updates

### WebSocket Bağlantısı

Dashboard otomatik olarak WebSocket kullanarak real-time güncellemeler alır:

```javascript
// Örnek WebSocket kullanımı
ws://localhost:8000/ws
```

**Gelen Event Tipleri:**
- `company_started` - Şirket başladı
- `company_stopped` - Şirket durdu
- `task_created` - Yeni görev
- `goal_added` - Yeni hedef
- `meeting_started` - Toplantı başladı
- `simulation_started` - Simülasyon başladı

---

## 🎯 Özellik Highlights

### ✨ Akıllı AI Dağılımı
- **Yazılım Ekibi** → Claude (daha iyi kod)
- **Marketing** → GPT-4 (daha kreatif)
- **Destek** → GPT-3.5 (hızlı ve ekonomik)

### 📈 Canlı İstatistikler
- Departman dağılımı grafikleri
- Görev durum grafikleri
- AI kullanım istatistikleri
- Hedef ilerleme takibi

### 🔄 Otomatik Yenileme
- 1-30 saniye aralıklarla
- Arka planda veri güncellemesi
- Kesintisiz izleme

---

## 🛠️ Geliştirici Notları

### Dosya Yapısı

```
/tmp/workspace/
├── dashboard/
│   ├── streamlit_app.py       # Ana dashboard
│   └── pages/
│       ├── 1_Live_Monitor.py  # Canlı izleme
│       └── 2_Control_Panel.py # Kontrol paneli
├── api/
│   └── main.py                # FastAPI backend
├── start_web.sh               # Başlatma scripti (Linux/Mac)
└── start_web.bat              # Başlatma scripti (Windows)
```

### Port Yapılandırması

- **Streamlit:** 8501 (varsayılan)
- **FastAPI:** 8000 (varsayılan)

Değiştirmek için:
```bash
# Streamlit
streamlit run app.py --server.port 9000

# FastAPI
uvicorn api.main:app --port 9000
```

---

## 🐛 Sorun Giderme

### Problem: API'ye bağlanılamıyor

**Çözüm:**
```bash
# API'nin çalışıp çalışmadığını kontrol et
curl http://localhost:8000/health

# Manuel başlat
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Problem: Streamlit açılmıyor

**Çözüm:**
```bash
# Port'u kontrol et
lsof -i :8501

# Farklı port dene
streamlit run dashboard/streamlit_app.py --server.port 8502
```

### Problem: Paketler yüklü değil

**Çözüm:**
```bash
pip install -r requirements.txt
```

---

## 📞 Destek

Sorunlarınız için:
1. `/health` endpoint'ini kontrol edin
2. Terminal loglarını inceleyin
3. API dokümantasyonuna bakın: http://localhost:8000/docs

---

## 🎉 Başarıyla Kurulduysa

Dashboard'da şunları görmelisiniz:
- ✅ 50+ AI çalışan
- ✅ 8 departman
- ✅ Aktif hedefler
- ✅ Canlı istatistikler

**Keyifli kullanımlar! 🚀**
