"""
🌐 Otonom AI Şirketi - FastAPI Backend
REST API ve WebSocket desteği ile şirket operasyonlarını yönetin
"""

from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys

# Proje root'unu path'e ekle
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.company import AutonomousCompany
from systems.ai_provider import get_ai_provider, AIProvider
from systems.auto_config import get_auto_configurator

# FastAPI uygulaması
app = FastAPI(
    title="Otonom AI Şirketi API",
    description="50+ AI çalışanı yöneten otonom şirket yönetim sistemi",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global şirket instance
company: Optional[AutonomousCompany] = None
company_running = False
active_websockets: List[WebSocket] = []

# Pydantic modelleri
class APIKeyConfig(BaseModel):
    openai_key: Optional[str] = None
    anthropic_key: Optional[str] = None
    google_key: Optional[str] = None

class Goal(BaseModel):
    title: str
    description: str
    department: str
    priority: int = 5
    metrics: Optional[Dict[str, Any]] = None

class Message(BaseModel):
    agent_name: str
    content: str
    recipient: Optional[str] = None

class TaskCreate(BaseModel):
    title: str
    description: str
    agent_name: Optional[str] = None
    priority: int = 5

# Yardımcı fonksiyonlar
async def broadcast_update(data: dict):
    """Tüm WebSocket bağlantılarına güncelleme gönder"""
    disconnected = []
    for websocket in active_websockets:
        try:
            await websocket.send_json(data)
        except Exception as e:
            disconnected.append(websocket)
    
    # Kopan bağlantıları temizle
    for ws in disconnected:
        active_websockets.remove(ws)

def get_company_status():
    """Şirketin mevcut durumunu döndür"""
    if not company:
        return {
            "status": "stopped",
            "message": "Şirket başlatılmamış"
        }
    
    return {
        "status": "running" if company_running else "idle",
        "total_agents": len(company.agents),
        "departments": len(set(a.department for a in company.agents)),
        "total_goals": len(company.goal_manager.goals),
        "completed_goals": len([g for g in company.goal_manager.goals if g.status == 'completed'])
    }

# API Endpoints

@app.get("/")
async def root():
    """API ana sayfa"""
    return {
        "name": "Otonom AI Şirketi API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "status": "/api/status",
            "agents": "/api/agents",
            "tasks": "/api/tasks",
            "goals": "/api/goals",
            "meetings": "/api/meetings",
            "start": "/api/start",
            "stop": "/api/stop"
        }
    }

@app.get("/api/status")
async def get_status():
    """Şirket durumu"""
    return get_company_status()

@app.post("/api/configure")
async def configure_api_keys(config: APIKeyConfig):
    """API anahtarlarını yapılandır"""
    try:
        env_file = ROOT_DIR / '.env'
        
        with open(env_file, 'w') as f:
            if config.openai_key:
                f.write(f"OPENAI_API_KEY={config.openai_key}\n")
            if config.anthropic_key:
                f.write(f"ANTHROPIC_API_KEY={config.anthropic_key}\n")
            if config.google_key:
                f.write(f"GOOGLE_API_KEY={config.google_key}\n")
        
        await broadcast_update({
            "type": "config_updated",
            "timestamp": datetime.now().isoformat()
        })
        
        return {"message": "API anahtarları başarıyla kaydedildi"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/start")
async def start_company(background_tasks: BackgroundTasks):
    """Şirketi başlat"""
    global company, company_running
    
    if company:
        return {"message": "Şirket zaten çalışıyor"}
    
    try:
        # AI Provider oluştur (auto-mode ile)
        ai_manager = get_ai_provider(auto_mode=True)
        
        # Şirketi oluştur
        company = AutonomousCompany(
            config_path=ROOT_DIR / 'config' / 'company_config.yaml'
        )
        
        # Initialize
        company.initialize()
        company_running = True
        
        await broadcast_update({
            "type": "company_started",
            "timestamp": datetime.now().isoformat(),
            "agents": len(company.agents)
        })
        
        return {
            "message": "Şirket başarıyla başlatıldı",
            "agents": len(company.agents),
            "departments": len(set(a.department for a in company.agents)),
            "goals": len(company.goal_manager.goals)
        }
    
    except Exception as e:
        company = None
        company_running = False
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stop")
async def stop_company():
    """Şirketi durdur"""
    global company, company_running
    
    if not company:
        return {"message": "Şirket zaten durmuş"}
    
    company_running = False
    company = None
    
    await broadcast_update({
        "type": "company_stopped",
        "timestamp": datetime.now().isoformat()
    })
    
    return {"message": "Şirket durduruldu"}

@app.get("/api/agents")
async def get_agents(department: Optional[str] = None):
    """Tüm çalışanları listele"""
    if not company:
        raise HTTPException(status_code=400, detail="Şirket başlatılmamış")
    
    agents = company.agents
    
    if department:
        agents = [a for a in agents if a.department == department]
    
    return {
        "total": len(agents),
        "agents": [
            {
                "name": agent.name,
                "role": agent.role,
                "department": agent.department,
                "skills": agent.skills,
                "assigned_ai": getattr(agent, 'assigned_ai', None),
                "completed_tasks": len(agent.memory.completed_tasks),
                "messages": len(agent.memory.messages)
            }
            for agent in agents
        ]
    }

@app.get("/api/agents/{agent_name}")
async def get_agent_details(agent_name: str):
    """Belirli bir çalışanın detayları"""
    if not company:
        raise HTTPException(status_code=400, detail="Şirket başlatılmamış")
    
    agent = next((a for a in company.agents if a.name == agent_name), None)
    
    if not agent:
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı")
    
    return {
        "name": agent.name,
        "role": agent.role,
        "department": agent.department,
        "skills": agent.skills,
        "assigned_ai": getattr(agent, 'assigned_ai', None),
        "completed_tasks": [
            {
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at.isoformat()
            }
            for task in agent.memory.completed_tasks
        ],
        "recent_messages": [
            {
                "sender": msg.sender,
                "recipient": msg.recipient,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in agent.memory.messages[-10:]
        ]
    }

@app.get("/api/tasks")
async def get_tasks(status: Optional[str] = None):
    """Tüm görevleri listele"""
    if not company:
        raise HTTPException(status_code=400, detail="Şirket başlatılmamış")
    
    all_tasks = []
    for agent in company.agents:
        for task in agent.memory.completed_tasks:
            all_tasks.append({
                "agent": agent.name,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at.isoformat()
            })
    
    if status:
        all_tasks = [t for t in all_tasks if t['status'] == status]
    
    return {
        "total": len(all_tasks),
        "tasks": sorted(all_tasks, key=lambda x: x['created_at'], reverse=True)
    }

@app.post("/api/tasks")
async def create_task(task: TaskCreate):
    """Yeni görev oluştur"""
    if not company:
        raise HTTPException(status_code=400, detail="Şirket başlatılmamış")
    
    # Görev oluştur ve ata
    if task.agent_name:
        agent = next((a for a in company.agents if a.name == task.agent_name), None)
        if not agent:
            raise HTTPException(status_code=404, detail="Çalışan bulunamadı")
    else:
        # Rastgele bir çalışana ata
        agent = company.agents[0]
    
    from agents.base_agent import Task
    
    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        assigned_to=agent.name
    )
    
    agent.receive_task(new_task)
    
    await broadcast_update({
        "type": "task_created",
        "task": task.title,
        "agent": agent.name,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "message": "Görev oluşturuldu",
        "task": task.title,
        "assigned_to": agent.name
    }

@app.get("/api/goals")
async def get_goals():
    """Tüm hedefleri listele"""
    if not company:
        raise HTTPException(status_code=400, detail="Şirket başlatılmamış")
    
    goals = company.goal_manager.goals
    
    return {
        "total": len(goals),
        "goals": [
            {
                "title": goal.title,
                "description": goal.description,
                "department": goal.department,
                "priority": goal.priority,
                "status": goal.status,
                "progress": goal.progress,
                "metrics": goal.metrics,
                "deadline": goal.deadline.isoformat() if goal.deadline else None
            }
            for goal in goals
        ]
    }

@app.post("/api/goals")
async def add_goal(goal: Goal):
    """Yeni hedef ekle"""
    if not company:
        raise HTTPException(status_code=400, detail="Şirket başlatılmamış")
    
    from systems.goals import Goal as GoalModel
    
    new_goal = GoalModel(
        title=goal.title,
        description=goal.description,
        department=goal.department,
        priority=goal.priority,
        metrics=goal.metrics or {}
    )
    
    company.goal_manager.goals.append(new_goal)
    company.goal_manager.save_goals()
    
    await broadcast_update({
        "type": "goal_added",
        "goal": goal.title,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "message": "Hedef eklendi",
        "goal": goal.title
    }

@app.get("/api/meetings")
async def get_meetings():
    """Toplantı kayıtlarını getir"""
    if not company:
        raise HTTPException(status_code=400, detail="Şirket başlatılmamış")
    
    meetings = company.meeting_system.meetings
    
    return {
        "total": len(meetings),
        "meetings": [
            {
                "title": meeting.title,
                "type": meeting.type,
                "date": meeting.date.isoformat(),
                "participants": meeting.participants,
                "notes": meeting.notes,
                "decisions": meeting.decisions,
                "action_items": meeting.action_items
            }
            for meeting in meetings
        ]
    }

@app.post("/api/meetings/standup")
async def run_standup(background_tasks: BackgroundTasks):
    """Günlük standup toplantısı yap"""
    if not company:
        raise HTTPException(status_code=400, detail="Şirket başlatılmamış")
    
    # Arka planda çalıştır
    def run_meeting():
        company.morning_standup()
    
    background_tasks.add_task(run_meeting)
    
    await broadcast_update({
        "type": "meeting_started",
        "meeting_type": "standup",
        "timestamp": datetime.now().isoformat()
    })
    
    return {"message": "Günlük toplantı başlatıldı"}

@app.post("/api/simulate/day")
async def simulate_day(background_tasks: BackgroundTasks):
    """Bir iş günü simüle et"""
    if not company:
        raise HTTPException(status_code=400, detail="Şirket başlatılmamış")
    
    def run_simulation():
        company.simulate_work_day()
    
    background_tasks.add_task(run_simulation)
    
    await broadcast_update({
        "type": "simulation_started",
        "simulation_type": "work_day",
        "timestamp": datetime.now().isoformat()
    })
    
    return {"message": "İş günü simülasyonu başlatıldı"}

@app.get("/api/departments")
async def get_departments():
    """Tüm departmanları listele"""
    if not company:
        raise HTTPException(status_code=400, detail="Şirket başlatılmamış")
    
    departments = {}
    for agent in company.agents:
        dept = agent.department
        if dept not in departments:
            departments[dept] = {
                "name": dept,
                "employees": [],
                "total": 0
            }
        
        departments[dept]["employees"].append({
            "name": agent.name,
            "role": agent.role
        })
        departments[dept]["total"] += 1
    
    return {
        "total": len(departments),
        "departments": list(departments.values())
    }

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket bağlantısı - real-time güncellemeler"""
    await websocket.accept()
    active_websockets.append(websocket)
    
    try:
        # İlk bağlantıda mevcut durumu gönder
        await websocket.send_json({
            "type": "connected",
            "status": get_company_status(),
            "timestamp": datetime.now().isoformat()
        })
        
        # Bağlantı canlı kalsın
        while True:
            data = await websocket.receive_text()
            
            # Ping-pong için
            if data == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })
    
    except Exception as e:
        if websocket in active_websockets:
            active_websockets.remove(websocket)

@app.get("/api/stats")
async def get_statistics():
    """Detaylı istatistikler"""
    if not company:
        raise HTTPException(status_code=400, detail="Şirket başlatılmamış")
    
    # Departman dağılımı
    dept_distribution = {}
    for agent in company.agents:
        dept_distribution[agent.department] = dept_distribution.get(agent.department, 0) + 1
    
    # Görev istatistikleri
    all_tasks = []
    for agent in company.agents:
        all_tasks.extend(agent.memory.completed_tasks)
    
    task_stats = {
        "pending": len([t for t in all_tasks if t.status == 'pending']),
        "in_progress": len([t for t in all_tasks if t.status == 'in_progress']),
        "completed": len([t for t in all_tasks if t.status == 'completed'])
    }
    
    # AI kullanımı
    ai_usage = {}
    for agent in company.agents:
        if hasattr(agent, 'assigned_ai'):
            model = agent.assigned_ai.get('model', 'Unknown')
            ai_usage[model] = ai_usage.get(model, 0) + 1
    
    return {
        "total_agents": len(company.agents),
        "total_departments": len(dept_distribution),
        "department_distribution": dept_distribution,
        "task_statistics": task_stats,
        "total_tasks": len(all_tasks),
        "ai_usage": ai_usage,
        "total_goals": len(company.goal_manager.goals),
        "completed_goals": len([g for g in company.goal_manager.goals if g.status == 'completed']),
        "total_meetings": len(company.meeting_system.meetings)
    }

# Health check
@app.get("/health")
async def health_check():
    """Sistem sağlık kontrolü"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "company_running": company is not None,
        "active_websockets": len(active_websockets)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
