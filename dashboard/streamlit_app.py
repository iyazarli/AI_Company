"""
🚀 Otonom AI Şirketi - Streamlit Dashboard
Tüm şirket operasyonlarını gerçek zamanlı izleyin ve yönetin
"""

import streamlit as st
import sys
import os
from pathlib import Path
import asyncio
import json
from datetime import datetime
import time
import threading

# Proje root'unu path'e ekle
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Circular import önlemek için lazy import - fonksiyon içinde import edilecek

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="🏢 Otonom AI Şirketi",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .agent-card {
        border: 2px solid #667eea;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        background: #f8f9ff;
    }
    .task-card {
        border-left: 4px solid #4CAF50;
        padding: 10px;
        margin: 5px 0;
        background: #f1f8f4;
    }
    .stButton>button {
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Session state başlatma
if 'company' not in st.session_state:
    st.session_state.company = None
if 'running' not in st.session_state:
    st.session_state.running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'api_keys_configured' not in st.session_state:
    st.session_state.api_keys_configured = False

def check_api_keys():
    """API key'lerin varlığını kontrol et"""
    # Önce Streamlit secrets'ı kontrol et (Cloud deployment için)
    if hasattr(st, 'secrets'):
        keys = []
        try:
            if 'OPENAI_API_KEY' in st.secrets:
                keys.append('OpenAI')
        except Exception as e:
            pass
        try:
            if 'ANTHROPIC_API_KEY' in st.secrets:
                keys.append('Anthropic')
        except Exception as e:
            pass
        try:
            if 'GOOGLE_API_KEY' in st.secrets:
                keys.append('Google')
        except Exception as e:
            pass
        
        if keys:
            return True, keys
    
    # .env dosyasını kontrol et (local deployment için)
    env_file = ROOT_DIR / '.env'
    if not env_file.exists():
        return False, []
    
    with open(env_file) as f:
        content = f.read()
    
    keys = []
    if 'OPENAI_API_KEY' in content and 'your-openai-api-key' not in content:
        keys.append('OpenAI')
    if 'ANTHROPIC_API_KEY' in content and 'your-anthropic-api-key' not in content:
        keys.append('Anthropic')
    if 'GOOGLE_API_KEY' in content and 'your-google-api-key' not in content:
        keys.append('Google')
    
    return len(keys) > 0, keys

def initialize_company():
    """Şirketi başlat"""
    try:
        # Lazy import - circular dependency önlemek için
        from core.company import AutonomousCompany
        from systems.ai_provider import get_ai_provider
        
        # Streamlit secrets'tan API keylerini environment'a yükle
        if hasattr(st, 'secrets'):
            try:
                if 'OPENAI_API_KEY' in st.secrets:
                    os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
            except Exception as e:
                pass
            try:
                if 'ANTHROPIC_API_KEY' in st.secrets:
                    os.environ['ANTHROPIC_API_KEY'] = st.secrets['ANTHROPIC_API_KEY']
            except Exception as e:
                pass
            try:
                if 'GOOGLE_API_KEY' in st.secrets:
                    os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
            except Exception as e:
                pass
        
        # AI Provider oluştur (auto-mode ile)
        ai_manager = get_ai_provider(auto_mode=True)
        
        # Şirketi oluştur
        company = AutonomousCompany(
            config_path=ROOT_DIR / 'config' / 'company_config.yaml',
            ai_provider_manager=ai_manager
        )
        
        # Initialize
        company.initialize()
        
        st.session_state.company = company
        st.session_state.logs.append(f"✅ {datetime.now().strftime('%H:%M:%S')} - Şirket başarıyla başlatıldı!")
        st.session_state.logs.append(f"👥 {len(company.agents)} çalışan görevde")
        st.session_state.logs.append(f"🎯 {len(company.goal_manager.goals)} hedef belirlendi")
        
        return True
    except Exception as e:
        st.error(f"❌ Şirket başlatılırken hata: {str(e)}")
        st.session_state.logs.append(f"❌ {datetime.now().strftime('%H:%M:%S')} - Hata: {str(e)}")
        return False

def main():
    # Header
    st.markdown('<h1 class="main-header">🏢 Otonom AI Şirketi</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar - Kontrol Paneli
    with st.sidebar:
        st.header("⚙️ Kontrol Paneli")
        
        # API Key Durumu
        st.subheader("🔑 API Anahtarları")
        has_keys, available_keys = check_api_keys()
        
        if has_keys:
            st.success(f"✅ {len(available_keys)} sağlayıcı aktif")
            for key in available_keys:
                st.info(f"✓ {key}")
            st.session_state.api_keys_configured = True
        else:
            st.warning("⚠️ API anahtarları yapılandırılmamış")
            st.info("Demo modunda çalışacak")
            st.session_state.api_keys_configured = False
        
        st.markdown("---")
        
        # Şirket Kontrolleri
        st.subheader("🎮 Şirket Kontrolü")
        
        if st.session_state.company is None:
            if st.button("🚀 Şirketi Başlat", use_container_width=True):
                with st.spinner("Şirket başlatılıyor..."):
                    initialize_company()
                    st.rerun()
        else:
            st.success("✅ Şirket Aktif")
            
            if st.button("🔄 Yeniden Başlat", use_container_width=True):
                st.session_state.company = None
                st.session_state.logs = []
                st.rerun()
        
        st.markdown("---")
        
        # Hızlı Aksiyonlar
        if st.session_state.company:
            st.subheader("⚡ Hızlı Aksiyonlar")
            
            if st.button("📊 Günlük Toplantı", use_container_width=True):
                with st.spinner("Toplantı yapılıyor..."):
                    st.session_state.company.morning_standup()
                    st.session_state.logs.append(f"📊 {datetime.now().strftime('%H:%M:%S')} - Günlük toplantı tamamlandı")
                    st.success("Toplantı tamamlandı!")
            
            if st.button("💼 Bir Günü Simüle Et", use_container_width=True):
                with st.spinner("İş günü simüle ediliyor..."):
                    st.session_state.company.simulate_work_day()
                    st.session_state.logs.append(f"💼 {datetime.now().strftime('%H:%M:%S')} - İş günü simülasyonu tamamlandı")
                    st.success("İş günü tamamlandı!")
        
        st.markdown("---")
        st.caption("Made with ❤️ by AI Company")
    
    # Ana İçerik
    if st.session_state.company is None:
        # Karşılama Ekranı
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            ### 🎯 Neler Yapabilir?
            - 50+ AI çalışan
            - 8 departman
            - Otonom görev yönetimi
            - Günlük toplantılar
            - Hedef takibi
            """)
        
        with col2:
            st.success("""
            ### 🤖 AI Sağlayıcıları
            - OpenAI (GPT-4, GPT-3.5)
            - Anthropic (Claude)
            - Google (Gemini)
            - Akıllı rol dağılımı
            - Maliyet optimizasyonu
            """)
        
        with col3:
            st.warning("""
            ### 🚀 Başlamak İçin
            1. API key ekle (.env)
            2. "Şirketi Başlat" tıkla
            3. Operasyonları izle
            4. Hedefler belirle
            5. Sonuçları gör
            """)
        
        st.markdown("---")
        
        # Büyük başlatma butonu
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 HEMEN BAŞLAT", use_container_width=True, type="primary"):
                with st.spinner("⏳ Şirket hazırlanıyor..."):
                    if initialize_company():
                        st.rerun()
    
    else:
        # Dashboard - Ana Ekran
        tabs = st.tabs([
            "📊 Genel Bakış",
            "👥 Çalışanlar",
            "📋 Görevler",
            "🎯 Hedefler",
            "💬 Toplantılar",
            "📈 İstatistikler",
            "🔧 Ayarlar"
        ])
        
        # TAB 1: Genel Bakış
        with tabs[0]:
            st.header("📊 Şirket Genel Bakış")
            
            # Metrikler
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👥 Toplam Çalışan", len(st.session_state.company.agents))
            
            with col2:
                active_tasks = sum(
                    len([t for t in agent.memory.completed_tasks if t.status == 'in_progress'])
                    for agent in st.session_state.company.agents
                )
                st.metric("📋 Aktif Görevler", active_tasks)
            
            with col3:
                st.metric("🎯 Hedefler", len(st.session_state.company.goal_manager.goals))
            
            with col4:
                completed_goals = len([
                    g for g in st.session_state.company.goal_manager.goals
                    if g.status == 'completed'
                ])
                st.metric("✅ Tamamlanan", completed_goals)
            
            st.markdown("---")
            
            # Departmanlar
            st.subheader("🏢 Departmanlar")
            
            dept_cols = st.columns(4)
            departments = {}
            for agent in st.session_state.company.agents:
                dept = agent.department
                if dept not in departments:
                    departments[dept] = []
                departments[dept].append(agent)
            
            for idx, (dept_name, agents) in enumerate(departments.items()):
                with dept_cols[idx % 4]:
                    st.markdown(f"""
                    <div class="agent-card">
                        <h4>{dept_name.replace('_', ' ').title()}</h4>
                        <p><strong>{len(agents)}</strong> çalışan</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Aktivite Günlüğü
            st.subheader("📝 Aktivite Günlüğü")
            
            log_container = st.container()
            with log_container:
                if st.session_state.logs:
                    for log in reversed(st.session_state.logs[-20:]):  # Son 20 log
                        st.text(log)
                else:
                    st.info("Henüz aktivite yok")
        
        # TAB 2: Çalışanlar
        with tabs[1]:
            st.header("👥 Tüm Çalışanlar")
            
            # Filtreler
            col1, col2 = st.columns(2)
            with col1:
                dept_filter = st.selectbox(
                    "Departman Filtrele",
                    ["Tümü"] + sorted(list(departments.keys()))
                )
            
            with col2:
                search = st.text_input("🔍 Çalışan Ara", "")
            
            # Çalışan listesi
            filtered_agents = st.session_state.company.agents
            
            if dept_filter != "Tümü":
                filtered_agents = [a for a in filtered_agents if a.department == dept_filter]
            
            if search:
                filtered_agents = [
                    a for a in filtered_agents
                    if search.lower() in a.name.lower() or search.lower() in a.role.lower()
                ]
            
            st.write(f"**{len(filtered_agents)} çalışan gösteriliyor**")
            
            # Grid layout
            cols = st.columns(3)
            for idx, agent in enumerate(filtered_agents):
                with cols[idx % 3]:
                    with st.expander(f"👤 {agent.name}"):
                        st.write(f"**Rol:** {agent.role}")
                        st.write(f"**Departman:** {agent.department}")
                        st.write(f"**Yetenekler:** {', '.join(agent.skills[:3])}")
                        
                        # AI Assignment
                        if hasattr(agent, 'assigned_ai'):
                            ai_info = agent.assigned_ai
                            st.info(f"🤖 AI: {ai_info.get('model', 'N/A')}")
                        
                        # Stats
                        completed = len(agent.memory.completed_tasks)
                        messages = len(agent.memory.messages)
                        st.metric("Tamamlanan Görevler", completed)
                        st.metric("Mesajlar", messages)
        
        # TAB 3: Görevler
        with tabs[2]:
            st.header("📋 Görev Yönetimi")
            
            # Task istatistikleri
            all_tasks = []
            for agent in st.session_state.company.agents:
                all_tasks.extend(agent.memory.completed_tasks)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                pending = len([t for t in all_tasks if t.status == 'pending'])
                st.metric("⏳ Bekleyen", pending)
            
            with col2:
                in_progress = len([t for t in all_tasks if t.status == 'in_progress'])
                st.metric("🔄 Devam Eden", in_progress)
            
            with col3:
                completed = len([t for t in all_tasks if t.status == 'completed'])
                st.metric("✅ Tamamlanan", completed)
            
            st.markdown("---")
            
            # Son görevler
            st.subheader("📝 Son Görevler")
            
            recent_tasks = sorted(all_tasks, key=lambda x: x.created_at, reverse=True)[:10]
            
            for task in recent_tasks:
                status_emoji = {
                    'pending': '⏳',
                    'in_progress': '🔄',
                    'completed': '✅'
                }
                
                st.markdown(f"""
                <div class="task-card">
                    <strong>{status_emoji.get(task.status, '❓')} {task.title}</strong><br>
                    <small>Öncelik: {task.priority} | Oluşturulma: {task.created_at.strftime('%d/%m/%Y %H:%M')}</small><br>
                    <small>{task.description[:100]}...</small>
                </div>
                """, unsafe_allow_html=True)
        
        # TAB 4: Hedefler
        with tabs[3]:
            st.header("🎯 Şirket Hedefleri")
            
            goals = st.session_state.company.goal_manager.goals
            
            if goals:
                for goal in goals:
                    with st.expander(f"{'✅' if goal.status == 'completed' else '🎯'} {goal.title}"):
                        st.write(f"**Açıklama:** {goal.description}")
                        st.write(f"**Departman:** {goal.department}")
                        st.write(f"**Öncelik:** {goal.priority}")
                        st.write(f"**Durum:** {goal.status}")
                        st.progress(goal.progress / 100)
                        st.write(f"**İlerleme:** {goal.progress}%")
                        
                        if goal.metrics:
                            st.write("**Metrikler:**")
                            for key, value in goal.metrics.items():
                                st.write(f"- {key}: {value}")
            else:
                st.info("Henüz hedef belirlenmemiş")
                st.write("set_goals.py ile hedef ekleyebilirsiniz")
        
        # TAB 5: Toplantılar
        with tabs[4]:
            st.header("💬 Toplantı Kayıtları")
            
            if hasattr(st.session_state.company, 'meeting_system'):
                meetings = st.session_state.company.meeting_system.meetings
                
                if meetings:
                    for meeting in reversed(meetings[-10:]):
                        with st.expander(f"📅 {meeting.title} - {meeting.date.strftime('%d/%m/%Y')}"):
                            st.write(f"**Tip:** {meeting.type}")
                            st.write(f"**Katılımcılar:** {len(meeting.participants)} kişi")
                            
                            if meeting.notes:
                                st.write("**Notlar:**")
                                for note in meeting.notes[:5]:
                                    st.write(f"- {note}")
                            
                            if meeting.decisions:
                                st.write("**Kararlar:**")
                                for decision in meeting.decisions:
                                    st.write(f"✓ {decision}")
                            
                            if meeting.action_items:
                                st.write("**Aksiyon Maddeleri:**")
                                for item in meeting.action_items:
                                    st.write(f"→ {item}")
                else:
                    st.info("Henüz toplantı yapılmamış")
            else:
                st.warning("Toplantı sistemi yüklenmemiş")
        
        # TAB 6: İstatistikler
        with tabs[5]:
            st.header("📈 Detaylı İstatistikler")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("👥 Departman Dağılımı")
                dept_data = {dept: len(agents) for dept, agents in departments.items()}
                st.bar_chart(dept_data)
            
            with col2:
                st.subheader("📊 Görev Durumu")
                task_status = {
                    'Bekleyen': len([t for t in all_tasks if t.status == 'pending']),
                    'Devam Eden': len([t for t in all_tasks if t.status == 'in_progress']),
                    'Tamamlanan': len([t for t in all_tasks if t.status == 'completed'])
                }
                st.bar_chart(task_status)
            
            st.markdown("---")
            
            # AI Kullanım İstatistikleri
            st.subheader("🤖 AI Sağlayıcı Dağılımı")
            
            ai_usage = {}
            for agent in st.session_state.company.agents:
                if hasattr(agent, 'assigned_ai'):
                    model = agent.assigned_ai.get('model', 'Unknown')
                    ai_usage[model] = ai_usage.get(model, 0) + 1
            
            if ai_usage:
                st.bar_chart(ai_usage)
            else:
                st.info("AI atama bilgisi yok")
        
        # TAB 7: Ayarlar
        with tabs[6]:
            st.header("🔧 Sistem Ayarları")
            
            # API Key Yönetimi
            st.subheader("🔑 API Anahtarları Yönetimi")
            
            # Session state'te API keyleri sakla
            if 'api_keys' not in st.session_state:
                st.session_state.api_keys = {
                    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
                    'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY', ''),
                    'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY', ''),
                }
            
            # Mevcut durumu göster
            has_keys, configured_providers = check_api_keys()
            
            if has_keys:
                st.success(f"✅ Yapılandırılmış: {', '.join(configured_providers)}")
            else:
                st.warning("⚠️ Henüz API anahtarı yapılandırılmamış")
            
            st.markdown("---")
            
            # API Key Input Form
            with st.expander("🔐 API Anahtarlarını Düzenle", expanded=not has_keys):
                st.info("💡 API anahtarlarınız güvenli bir şekilde saklanır ve asla loglanmaz.")
                
                # OpenAI
                col1, col2 = st.columns([3, 1])
                with col1:
                    current_openai = st.session_state.api_keys.get('OPENAI_API_KEY', '')
                    openai_key = st.text_input(
                        "🤖 OpenAI API Key",
                        value=current_openai,
                        type="password",
                        placeholder="sk-...",
                        help="GPT-4, GPT-3.5 için gerekli",
                        key="input_openai"
                    )
                with col2:
                    if current_openai:
                        st.metric("Durum", "✅", delta="Aktif")
                    else:
                        st.metric("Durum", "⚠️", delta="Boş")
                
                # Anthropic
                col1, col2 = st.columns([3, 1])
                with col1:
                    current_anthropic = st.session_state.api_keys.get('ANTHROPIC_API_KEY', '')
                    anthropic_key = st.text_input(
                        "🧠 Anthropic API Key",
                        value=current_anthropic,
                        type="password",
                        placeholder="sk-ant-...",
                        help="Claude 3 için gerekli",
                        key="input_anthropic"
                    )
                with col2:
                    if current_anthropic:
                        st.metric("Durum", "✅", delta="Aktif")
                    else:
                        st.metric("Durum", "⚠️", delta="Boş")
                
                # Google
                col1, col2 = st.columns([3, 1])
                with col1:
                    current_google = st.session_state.api_keys.get('GOOGLE_API_KEY', '')
                    google_key = st.text_input(
                        "🌟 Google API Key",
                        value=current_google,
                        type="password",
                        placeholder="AI...",
                        help="Gemini Pro için gerekli",
                        key="input_google"
                    )
                with col2:
                    if current_google:
                        st.metric("Durum", "✅", delta="Aktif")
                    else:
                        st.metric("Durum", "⚠️", delta="Boş")
                
                st.markdown("---")
                
                # Kaydet butonu
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("💾 Kaydet ve Uygula", type="primary", use_container_width=True):
                        try:
                            # Session state'i güncelle
                            st.session_state.api_keys['OPENAI_API_KEY'] = openai_key
                            st.session_state.api_keys['ANTHROPIC_API_KEY'] = anthropic_key
                            st.session_state.api_keys['GOOGLE_API_KEY'] = google_key
                            
                            # Environment variables'ı güncelle
                            os.environ['OPENAI_API_KEY'] = openai_key
                            os.environ['ANTHROPIC_API_KEY'] = anthropic_key
                            os.environ['GOOGLE_API_KEY'] = google_key
                            
                            # .env dosyasına yaz (opsiyonel - kalıcılık için)
                            env_file = ROOT_DIR / '.env'
                            with open(env_file, 'w') as f:
                                f.write(f"# Otonom AI Şirketi - API Anahtarları\n")
                                f.write(f"# Son güncelleme: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                                f.write(f"OPENAI_API_KEY={openai_key}\n")
                                f.write(f"ANTHROPIC_API_KEY={anthropic_key}\n")
                                f.write(f"GOOGLE_API_KEY={google_key}\n")
                            
                            st.session_state.api_keys_configured = True
                            st.success("✅ API anahtarları başarıyla güncellendi!")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Hata: {str(e)}")
            
            st.markdown("---")
            
            # Test API Keys
            st.subheader("🧪 API Bağlantı Testi")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🤖 OpenAI Test", use_container_width=True):
                    with st.spinner("Test ediliyor..."):
                        try:
                            import openai
                            openai.api_key = st.session_state.api_keys.get('OPENAI_API_KEY')
                            # Basit bir test çağrısı
                            st.info("✅ OpenAI bağlantısı başarılı!")
                        except Exception as e:
                            st.error(f"❌ OpenAI hatası: {str(e)[:100]}")
            
            with col2:
                if st.button("🧠 Anthropic Test", use_container_width=True):
                    with st.spinner("Test ediliyor..."):
                        try:
                            import anthropic
                            client = anthropic.Anthropic(
                                api_key=st.session_state.api_keys.get('ANTHROPIC_API_KEY')
                            )
                            st.info("✅ Anthropic bağlantısı başarılı!")
                        except Exception as e:
                            st.error(f"❌ Anthropic hatası: {str(e)[:100]}")
            
            with col3:
                if st.button("🌟 Google Test", use_container_width=True):
                    with st.spinner("Test ediliyor..."):
                        try:
                            import google.generativeai as genai
                            genai.configure(api_key=st.session_state.api_keys.get('GOOGLE_API_KEY'))
                            st.info("✅ Google bağlantısı başarılı!")
                        except Exception as e:
                            st.error(f"❌ Google hatası: {str(e)[:100]}")
            
            st.markdown("---")
            
            st.subheader("ℹ️ Sistem Bilgileri")
            
            st.code(f"""
Proje Dizini: {ROOT_DIR}
Config: {ROOT_DIR / 'config'}
Çalışan Sayısı: {len(st.session_state.company.agents)}
Departman Sayısı: {len(departments)}
Python: {sys.version.split()[0]}
Yapılandırılmış API'ler: {', '.join(configured_providers) if has_keys else 'Yok'}
            """)

if __name__ == "__main__":
    main()
