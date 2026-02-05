"""
📊 Real-Time Monitoring Dashboard
Şirket aktivitelerini canlı takip edin
"""

import streamlit as st
import sys
from pathlib import Path
import requests
import json
import time
from datetime import datetime
import pandas as pd

# Proje root'unu path'e ekle
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# API Base URL
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="🔴 Live Monitoring",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Real-Time Monitoring Dashboard")
st.markdown("---")

# API bağlantısını kontrol et
try:
    response = requests.get(f"{API_URL}/health", timeout=2)
    api_available = response.status_code == 200
except:
    api_available = False

if not api_available:
    st.error("⚠️ API sunucusu çalışmıyor! Lütfen önce API'yi başlatın:")
    st.code("cd /tmp/workspace && python api/main.py")
    st.stop()

# Auto-refresh seçeneği
auto_refresh = st.sidebar.checkbox("🔄 Otomatik Yenile", value=True)
refresh_interval = st.sidebar.slider("Yenileme Süresi (saniye)", 1, 30, 5)

# Şirket durumunu çek
try:
    status_response = requests.get(f"{API_URL}/api/status")
    status = status_response.json()
except:
    st.error("API'den veri alınamadı")
    st.stop()

# Üst metrikler
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏢 Durum",
        status.get('status', 'unknown').upper(),
        delta="Aktif" if status.get('status') == 'running' else "Pasif"
    )

with col2:
    st.metric("👥 Çalışan", status.get('total_agents', 0))

with col3:
    st.metric("🎯 Hedefler", status.get('total_goals', 0))

with col4:
    completed = status.get('completed_goals', 0)
    total = status.get('total_goals', 1)
    completion_rate = int((completed / total) * 100) if total > 0 else 0
    st.metric("✅ Tamamlanma", f"{completion_rate}%")

st.markdown("---")

# Ana içerik - 2 kolon
col_left, col_right = st.columns([2, 1])

with col_left:
    # Görev Akışı
    st.subheader("📋 Görev Akışı")
    
    try:
        tasks_response = requests.get(f"{API_URL}/api/tasks")
        tasks_data = tasks_response.json()
        
        if tasks_data['total'] > 0:
            # Görev durumu grafiği
            tasks = tasks_data['tasks']
            
            status_counts = {
                'Bekleyen': len([t for t in tasks if t['status'] == 'pending']),
                'Devam Eden': len([t for t in tasks if t['status'] == 'in_progress']),
                'Tamamlanan': len([t for t in tasks if t['status'] == 'completed'])
            }
            
            st.bar_chart(status_counts)
            
            # Son görevler tablosu
            st.write("**Son 10 Görev:**")
            recent_tasks = tasks[:10]
            
            task_df = pd.DataFrame([
                {
                    'Görev': t['title'],
                    'Çalışan': t['agent'],
                    'Durum': t['status'],
                    'Öncelik': t['priority'],
                    'Tarih': t['created_at'][:10]
                }
                for t in recent_tasks
            ])
            
            st.dataframe(task_df, use_container_width=True)
        else:
            st.info("Henüz görev yok")
    
    except Exception as e:
        st.error(f"Görevler yüklenemedi: {str(e)}")
    
    st.markdown("---")
    
    # Hedef Takibi
    st.subheader("🎯 Hedef Takibi")
    
    try:
        goals_response = requests.get(f"{API_URL}/api/goals")
        goals_data = goals_response.json()
        
        if goals_data['total'] > 0:
            for goal in goals_data['goals'][:5]:
                with st.expander(f"{'✅' if goal['status'] == 'completed' else '🎯'} {goal['title']}"):
                    st.write(f"**Departman:** {goal['department']}")
                    st.write(f"**Öncelik:** {goal['priority']}/10")
                    
                    progress = goal.get('progress', 0)
                    st.progress(progress / 100)
                    st.write(f"**İlerleme:** {progress}%")
        else:
            st.info("Henüz hedef belirlenmemiş")
    
    except Exception as e:
        st.error(f"Hedefler yüklenemedi: {str(e)}")

with col_right:
    # Canlı Aktivite Akışı
    st.subheader("🔴 Canlı Aktivite")
    
    activity_container = st.container()
    
    with activity_container:
        # Simüle edilmiş aktivite akışı
        st.info(f"🕐 {datetime.now().strftime('%H:%M:%S')} - Sistem izleniyor...")
        
        # Departman durumu
        st.write("**Departman Durumu:**")
        
        try:
            dept_response = requests.get(f"{API_URL}/api/departments")
            dept_data = dept_response.json()
            
            for dept in dept_data['departments'][:5]:
                st.write(f"• {dept['name']}: {dept['total']} çalışan")
        
        except:
            st.warning("Departman bilgisi alınamadı")
    
    st.markdown("---")
    
    # AI Kullanım İstatistikleri
    st.subheader("🤖 AI Dağılımı")
    
    try:
        stats_response = requests.get(f"{API_URL}/api/stats")
        stats = stats_response.json()
        
        ai_usage = stats.get('ai_usage', {})
        
        if ai_usage:
            for model, count in ai_usage.items():
                model_name = model.split('-')[0].upper()
                st.metric(model_name, count, delta=f"{int((count/stats['total_agents'])*100)}%")
        else:
            st.info("AI atama bilgisi yok")
    
    except:
        st.warning("İstatistikler alınamadı")
    
    st.markdown("---")
    
    # Hızlı Aksiyonlar
    st.subheader("⚡ Hızlı Aksiyonlar")
    
    if st.button("📊 Standup Toplantısı", use_container_width=True):
        try:
            requests.post(f"{API_URL}/api/meetings/standup")
            st.success("Toplantı başlatıldı!")
        except:
            st.error("Toplantı başlatılamadı")
    
    if st.button("💼 Bir Gün Simüle Et", use_container_width=True):
        try:
            requests.post(f"{API_URL}/api/simulate/day")
            st.success("Simülasyon başlatıldı!")
        except:
            st.error("Simülasyon başlatılamadı")

st.markdown("---")

# Toplantı Geçmişi
st.subheader("💬 Son Toplantılar")

try:
    meetings_response = requests.get(f"{API_URL}/api/meetings")
    meetings_data = meetings_response.json()
    
    if meetings_data['total'] > 0:
        for meeting in meetings_data['meetings'][:3]:
            with st.expander(f"📅 {meeting['title']} - {meeting['date'][:10]}"):
                st.write(f"**Tip:** {meeting['type']}")
                st.write(f"**Katılımcılar:** {len(meeting['participants'])} kişi")
                
                if meeting.get('decisions'):
                    st.write("**Kararlar:**")
                    for decision in meeting['decisions'][:3]:
                        st.write(f"✓ {decision}")
    else:
        st.info("Henüz toplantı yok")

except Exception as e:
    st.error(f"Toplantılar yüklenemedi: {str(e)}")

# Auto-refresh
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
