# 🚀 Hızlı Başlangıç Rehberi

## 3 Adımda Başlatın

### 1️⃣ API Key Alın (2 dakika)

**En az bir tane yeterli!**

**Önerilen: OpenAI** (En popüler)
1. https://platform.openai.com/api-keys adresine gidin
2. "Create new secret key" butonuna tıklayın
3. Anahtarı kopyalayın: `sk-...`

**Alternatif: Anthropic Claude** (Daha güçlü)
1. https://console.anthropic.com/ adresine gidin
2. API key oluşturun
3. Anahtarı kopyalayın: `sk-ant-...`

**Alternatif: Google Gemini** (Ücretsiz başlangıç)
1. https://makersuite.google.com/app/apikey adresine gidin
2. API key alın

### 2️⃣ Kurulum (1 dakika)

```bash
# Hızlı başlatma (önerilen)
chmod +x quick_start.sh
./quick_start.sh

# Windows için
quick_start.bat
```

### 3️⃣ API Key'i Ekleyin

Script `.env` dosyasını oluşturacak. Düzenleyin:

```bash
nano .env
# veya
code .env
```

En az birini ekleyin:
```
OPENAI_API_KEY=sk-...
```

Kaydedin ve çıkın!

## ✅ Başlatın

```bash
python main.py
```

Karşınıza menü çıkacak:
1. **Hızlı Demo** - 5 dakikada tüm özellikleri gör
2. **Tek Gün Simülasyonu** - Tam bir iş günü
3. **Sürekli Çalışma** - 7/24 mod
4. **Özel Senaryo** - İstediğiniz aktivite

## 🎯 Diğer Komutlar

```bash
# AI atamalarını gör
python show_ai_assignments.py

# Hedef belirle
python set_goals.py

# Dashboard
python dashboard.py

# Toplantı simüle et
python run_meeting.py --type daily-standup
```

## ❓ Sorun Giderme

**"API key bulunamadı" hatası:**
- `.env` dosyasının olduğundan emin olun
- API key'in doğru kopyalandığından emin olun
- `sk-` ile başlamalı (OpenAI için)

**"Module not found" hatası:**
```bash
pip install -r requirements.txt
```

**Demo modunda çalışıyor:**
- Hiç API key eklemediniz
- En az bir API key ekleyin ve tekrar başlatın

## 💡 İpuçları

- **Sadece OpenAI yeterli**: Tek API key ile tüm özellikler çalışır
- **Çoklu AI**: OpenAI + Anthropic eklerseniz, sistem otomatik optimal dağılım yapar
- **Ücretsiz Test**: Google Gemini ile ücretsiz başlayabilirsiniz

## 📊 Maliyet Tahmini

**Sadece OpenAI:**
- Free tier ile başlayabilirsiniz
- Tam kullanım: ~$50-200/ay

**OpenAI + Anthropic:**
- Optimal dağılım ile ~$100-500/ay

**Enterprise (hepsi):**
- ~$500-2000/ay

## 🆘 Yardım

Problem mi yaşıyorsunuz?
1. `.env` dosyasını kontrol edin
2. `python test_company.py` çalıştırın
3. Log dosyasına bakın: `data/logs/company.log`

Hazırsınız! 🎉
