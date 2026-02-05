@echo off
echo 🚀 Otonom AI Sirket - Hizli Baslatma
echo.

REM .env dosyasi kontrolu
if not exist .env (
    echo 📝 .env dosyasi olusturuluyor...
    copy .env.example .env
    echo.
    echo ⚠️  ONEMLI: .env dosyasini duzenleyin!
    echo.
    echo Asagidaki API key'lerden EN AZ BIRINI ekleyin:
    echo.
    echo 1. OpenAI (Onerilen):
    echo    https://platform.openai.com/api-keys
    echo    OPENAI_API_KEY=sk-...
    echo.
    echo 2. Anthropic (Istege bagli):
    echo    https://console.anthropic.com/
    echo    ANTHROPIC_API_KEY=sk-ant-...
    echo.
    echo 3. Google (Istege bagli):
    echo    https://makersuite.google.com/app/apikey
    echo    GOOGLE_API_KEY=...
    echo.
    echo Duzenlemek icin:
    echo   notepad .env
    echo.
    pause
)

REM Sanal ortam kontrolu
if not exist venv (
    echo 📦 Sanal ortam olusturuluyor...
    python -m venv venv
)

REM Aktiflestir
call venv\Scripts\activate.bat

REM Bagimliliklari kontrol et
if not exist venv\.dependencies_installed (
    echo 📥 Bagimliliklar yukleniyor...
    python -m pip install -q --upgrade pip
    pip install -q -r requirements.txt
    type nul > venv\.dependencies_installed
)

REM API key kontrolu
echo.
echo 🔍 API key'ler kontrol ediliyor...
python -c "from dotenv import load_dotenv; import os; load_dotenv(); has_key = bool(os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY') or os.getenv('GOOGLE_API_KEY')); print('✅ API key bulundu' if has_key else '⚠️ API key bulunamadi - Demo modunda calisacak')"

echo.
echo 🎯 Sirketi baslatmak icin:
echo   python main.py
echo.
echo 📊 Diger komutlar:
echo   python show_ai_assignments.py  - AI atamalarini gor
echo   python set_goals.py            - Hedef belirle
echo   python dashboard.py            - Dashboard
echo.

set /p choice="Simdi baslatmak ister misiniz? (y/n): "
if /i "%choice%"=="y" (
    python main.py
)

pause
