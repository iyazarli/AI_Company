@echo off
REM 🌐 Web Dashboard Başlatma Script'i (Windows)
REM Streamlit Dashboard ve FastAPI Backend'i başlatır

echo 🌐 Otonom AI Şirketi - Web Dashboard Başlatılıyor...
echo ==================================================

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Lütfen Python 3.8+ yükleyin.
    pause
    exit /b 1
)

echo ✓ Python bulundu

REM Virtual environment kontrolü
if not exist "venv" (
    echo ⚠️  Virtual environment bulunamadı
    echo Virtual environment oluşturmak ister misiniz? (Y/N)
    set /p response=
    if /i "%response%"=="Y" (
        echo 📦 Virtual environment oluşturuluyor...
        python -m venv venv
        echo ✓ Virtual environment oluşturuldu
    )
)

REM Virtual environment aktif et
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Virtual environment aktif ediliyor...
    call venv\Scripts\activate.bat
    echo ✓ Virtual environment aktif
)

REM Paket kontrolü
echo 📦 Paketler kontrol ediliyor...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Streamlit yüklü değil, yükleniyor...
    pip install -r requirements.txt
    echo ✓ Tüm paketler yüklendi
) else (
    echo ✓ Paketler hazır
)

REM .env dosyası kontrolü
if not exist ".env" (
    echo ⚠️  .env dosyası bulunamadı
    echo 📝 .env dosyası oluşturuluyor...
    
    if exist ".env.example" (
        copy .env.example .env
        echo ✓ .env dosyası oluşturuldu
    ) else (
        (
            echo OPENAI_API_KEY=your-openai-api-key
            echo ANTHROPIC_API_KEY=your-anthropic-api-key
            echo GOOGLE_API_KEY=your-google-api-key
        ) > .env
        echo ✓ .env dosyası oluşturuldu
    )
    
    echo ⚠️  Lütfen .env dosyasına API anahtarlarınızı ekleyin!
)

echo.
echo ==================================================
echo 🚀 Web Dashboard Başlatılıyor...
echo ==================================================
echo.

REM Port tanımları
set API_PORT=8000
set STREAMLIT_PORT=8501

echo 📡 API Backend başlatılıyor (Port: %API_PORT%)...

REM API'yi arka planda başlat
start "API Backend" /MIN python -m uvicorn api.main:app --host 0.0.0.0 --port %API_PORT% --reload

echo ✓ API Backend başlatıldı

REM API'nin hazır olmasını bekle
echo ⏳ API hazırlanıyor...
timeout /t 3 /nobreak >nul

echo.
echo 🎨 Streamlit Dashboard başlatılıyor (Port: %STREAMLIT_PORT%)...

REM Streamlit'i başlat
start "Streamlit Dashboard" streamlit run dashboard\streamlit_app.py --server.port %STREAMLIT_PORT% --server.headless false

echo ✓ Streamlit Dashboard başlatıldı

echo.
echo ==================================================
echo ✅ Web Dashboard Hazır!
echo ==================================================
echo.
echo 📊 Streamlit Dashboard: http://localhost:%STREAMLIT_PORT%
echo 🌐 FastAPI Backend:     http://localhost:%API_PORT%
echo 📚 API Docs:            http://localhost:%API_PORT%/docs
echo.
echo ⚡ Tarayıcınızda otomatik açılacak
echo ⚠️  Kapatmak için bu pencereyi kapatın
echo.

REM Tarayıcıda aç
timeout /t 2 /nobreak >nul
start http://localhost:%STREAMLIT_PORT%

pause
