"""
🎮 Interaktif Kontrol Paneli
Şirketi manuel olarak yönetin ve görevler atayın
"""

import streamlit as st
import requests
import json
from datetime import datetime

# API Base URL
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="🎮 Control Panel",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 İnteraktif Kontrol Paneli")
st.markdown("Şirket operasyonlarını manuel olarak yönetin")
st.markdown("---")

# API kontrolü
try:
    health = requests.get(f"{API_URL}/health", timeout=2)
    api_ok = health.status_code == 200
except:
    api_ok = False

if not api_ok:
    st.warning("⚠️ API sunucusu çalışmıyor. Sadece ana dashboard'u kullanın.")
    st.info("💡 Ana sayfaya dönün: Soldaki menüden 'streamlit app' seçin")
    st.markdown("---")
    st.markdown("""
    ### 🔧 API Olmadan Kullanım
    
    Kontrol paneli API backend gerektirir.
    
    **Ana Dashboard'da Yapabilirsiniz:**
    - ✅ Şirket başlatma/durdurma
    - ✅ Toplantı yapma
    - ✅ İş günü simülasyonu
    - ✅ İstatistik görüntüleme
    
    **Lokal Kullanım için:**
    ```bash
    ./start_web.sh
    ```
    """)
    st.stop()

# Tab'lar
tabs = st.tabs(["🎯 Hedef Ekle", "📋 Görev Oluştur", "💬 Mesaj Gönder", "⚙️ Şirket Kontrolü"])

# TAB 1: Hedef Ekle
with tabs[0]:
    st.header("🎯 Yeni Hedef Belirle")
    
    with st.form("goal_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            goal_title = st.text_input("Hedef Başlığı", placeholder="Örn: Yeni özellik geliştir")
            goal_dept = st.selectbox(
                "Departman",
                ["technology", "marketing", "sales", "finance", "hr", "customer_service", "management", "legal"]
            )
        
        with col2:
            goal_priority = st.slider("Öncelik", 1, 10, 5)
            goal_deadline = st.date_input("Hedef Tarih")
        
        goal_description = st.text_area("Detaylı Açıklama", height=150)
        
        # Metrikler
        st.subheader("📊 Ölçülebilir Metrikler (Opsiyonel)")
        
        metric_cols = st.columns(3)
        
        with metric_cols[0]:
            metric1_key = st.text_input("Metrik 1 Adı", placeholder="Örn: Kullanıcı Sayısı")
            metric1_val = st.text_input("Hedef Değer", placeholder="1000")
        
        with metric_cols[1]:
            metric2_key = st.text_input("Metrik 2 Adı", placeholder="Örn: Gelir")
            metric2_val = st.text_input("Hedef Değer ", placeholder="$50000")
        
        with metric_cols[2]:
            metric3_key = st.text_input("Metrik 3 Adı", placeholder="Örn: Tamamlanma")
            metric3_val = st.text_input("Hedef Değer  ", placeholder="100%")
        
        submitted = st.form_submit_button("✅ Hedef Ekle", use_container_width=True)
        
        if submitted:
            if goal_title and goal_description:
                # Metrikleri hazırla
                metrics = {}
                if metric1_key and metric1_val:
                    metrics[metric1_key] = metric1_val
                if metric2_key and metric2_val:
                    metrics[metric2_key] = metric2_val
                if metric3_key and metric3_val:
                    metrics[metric3_key] = metric3_val
                
                # API'ye gönder
                try:
                    response = requests.post(
                        f"{API_URL}/api/goals",
                        json={
                            "title": goal_title,
                            "description": goal_description,
                            "department": goal_dept,
                            "priority": goal_priority,
                            "metrics": metrics
                        }
                    )
                    
                    if response.status_code == 200:
                        st.success(f"✅ Hedef başarıyla eklendi: {goal_title}")
                    else:
                        st.error(f"❌ Hata: {response.text}")
                
                except Exception as e:
                    st.error(f"❌ API hatası: {str(e)}")
            else:
                st.warning("⚠️ Lütfen tüm zorunlu alanları doldurun")

# TAB 2: Görev Oluştur
with tabs[1]:
    st.header("📋 Yeni Görev Oluştur")
    
    # Önce çalışanları çek
    try:
        agents_response = requests.get(f"{API_URL}/api/agents")
        agents_data = agents_response.json()
        agents_list = [a['name'] for a in agents_data['agents']]
    except:
        st.error("Çalışan listesi alınamadı")
        agents_list = []
    
    with st.form("task_form"):
        task_title = st.text_input("Görev Başlığı", placeholder="Örn: API endpoint'i geliştir")
        task_description = st.text_area("Görev Detayı", height=150, placeholder="Ne yapılması gerekiyor?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            task_priority = st.slider("Öncelik Seviyesi", 1, 10, 5)
        
        with col2:
            task_agent = st.selectbox(
                "Atanacak Çalışan",
                ["Otomatik Seç"] + agents_list
            )
        
        task_submitted = st.form_submit_button("✅ Görevi Ata", use_container_width=True)
        
        if task_submitted:
            if task_title and task_description:
                try:
                    payload = {
                        "title": task_title,
                        "description": task_description,
                        "priority": task_priority
                    }
                    
                    if task_agent != "Otomatik Seç":
                        payload["agent_name"] = task_agent
                    
                    response = requests.post(f"{API_URL}/api/tasks", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ Görev oluşturuldu ve {result['assigned_to']} kişisine atandı")
                    else:
                        st.error(f"❌ Hata: {response.text}")
                
                except Exception as e:
                    st.error(f"❌ API hatası: {str(e)}")
            else:
                st.warning("⚠️ Lütfen görev başlığı ve detayını girin")

# TAB 3: Mesaj Gönder
with tabs[2]:
    st.header("💬 Çalışanlara Mesaj Gönder")
    
    st.info("🚧 Bu özellik yakında eklenecek")
    
    with st.form("message_form"):
        msg_sender = st.selectbox("Gönderen", agents_list if agents_list else ["CEO"])
        msg_recipient = st.selectbox("Alıcı", ["Tüm Şirket"] + agents_list if agents_list else ["Tüm Şirket"])
        msg_content = st.text_area("Mesaj İçeriği", height=200)
        
        msg_submitted = st.form_submit_button("📨 Mesaj Gönder", use_container_width=True)
        
        if msg_submitted:
            st.info("Mesaj gönderme özelliği yakında aktif olacak")

# TAB 4: Şirket Kontrolü
with tabs[3]:
    st.header("⚙️ Şirket Kontrolü")
    
    # Durum kontrolü
    try:
        status_response = requests.get(f"{API_URL}/api/status")
        status = status_response.json()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if status['status'] == 'running':
                st.success("✅ Şirket Aktif")
            else:
                st.warning("⏸️ Şirket Pasif")
        
        with col2:
            st.metric("Çalışan Sayısı", status.get('total_agents', 0))
        
        with col3:
            st.metric("Departman Sayısı", status.get('departments', 0))
    
    except:
        st.error("Durum bilgisi alınamadı")
    
    st.markdown("---")
    
    # Kontrol butonları
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Şirketi Başlat", use_container_width=True, type="primary"):
            try:
                response = requests.post(f"{API_URL}/api/start")
                if response.status_code == 200:
                    st.success("✅ Şirket başlatıldı!")
                    st.rerun()
                else:
                    st.error("Başlatma hatası")
            except Exception as e:
                st.error(f"Hata: {str(e)}")
    
    with col2:
        if st.button("⏹️ Şirketi Durdur", use_container_width=True):
            try:
                response = requests.post(f"{API_URL}/api/stop")
                if response.status_code == 200:
                    st.success("Şirket durduruldu")
                    st.rerun()
                else:
                    st.error("Durdurma hatası")
            except Exception as e:
                st.error(f"Hata: {str(e)}")
    
    st.markdown("---")
    
    # API Key Konfigürasyonu
    st.subheader("🔑 API Anahtarları")
    
    with st.form("api_config_form"):
        st.info("API anahtarlarınızı güvenli bir şekilde saklayın")
        
        openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
        anthropic_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
        google_key = st.text_input("Google API Key", type="password", placeholder="AIza...")
        
        config_submitted = st.form_submit_button("💾 Kaydet", use_container_width=True)
        
        if config_submitted:
            if openai_key or anthropic_key or google_key:
                try:
                    response = requests.post(
                        f"{API_URL}/api/configure",
                        json={
                            "openai_key": openai_key if openai_key else None,
                            "anthropic_key": anthropic_key if anthropic_key else None,
                            "google_key": google_key if google_key else None
                        }
                    )
                    
                    if response.status_code == 200:
                        st.success("✅ API anahtarları kaydedildi! Şirketi yeniden başlatın.")
                    else:
                        st.error("Kayıt hatası")
                
                except Exception as e:
                    st.error(f"Hata: {str(e)}")
            else:
                st.warning("En az bir API anahtarı girin")
    
    st.markdown("---")
    
    # Sistem Bilgileri
    st.subheader("ℹ️ Sistem Bilgileri")
    
    try:
        health_response = requests.get(f"{API_URL}/health")
        health_data = health_response.json()
        
        st.json(health_data)
    
    except:
        st.error("Sistem bilgisi alınamadı")
