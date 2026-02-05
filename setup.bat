@echo off
REM Otonom AI Sirket - Windows Kurulum Scripti

echo 🏢 Otonom AI Sirket Kurulumu Basliyor...
echo.

REM Python versiyonu kontrolu
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadi! Lutfen Python 3.8+ yukleyin.
    exit /b 1
)

echo ✅ Python bulundu
python --version
echo.

REM Sanal ortam olustur
echo 📦 Sanal ortam olusturuluyor...
python -m venv venv

REM Sanal ortami aktiflestir
echo 🔌 Sanal ortam aktiflestiriliyor...
call venv\Scripts\activate.bat

REM Bagimliliklari yukle
echo 📥 Bagimliliklar yukleniyor...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM .env dosyasi olustur
if not exist .env (
    echo 📝 .env dosyasi olusturuluyor...
    copy .env.example .env
    echo.
    echo ⚠️  ONEMLI: .env dosyasini duzenleyin ve API anahtarlarinizi ekleyin!
    echo    - OPENAI_API_KEY
    echo    - ANTHROPIC_API_KEY (opsiyonel)
)

REM Data klasorlerini olustur
echo 📁 Data klasorleri olusturuluyor...
if not exist data mkdir data
if not exist data\logs mkdir data\logs
if not exist data\tasks mkdir data\tasks
if not exist data\meetings mkdir data\meetings
if not exist data\reports mkdir data\reports

echo.
echo ✅ Kurulum tamamlandi!
echo.
echo 🚀 Baslatmak icin:
echo    venv\Scripts\activate.bat
echo    python main.py
echo.
echo 📊 Dashboard icin:
echo    python dashboard.py
echo.
echo 🎤 Toplanti simulasyonu icin:
echo    python run_meeting.py --type daily-standup
echo.

pause
