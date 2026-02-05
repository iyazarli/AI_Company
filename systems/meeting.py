"""
Meeting System - Toplantı yönetim sistemi
"""
from typing import List, Dict, Optional, TYPE_CHECKING
from datetime import datetime, time
from pydantic import BaseModel
import asyncio


import logging
logger = logging.getLogger(__name__)
# Circular import önlemek için TYPE_CHECKING kullan
if TYPE_CHECKING:
    from agents.ai_agent import AIAgent


class MeetingAgenda(BaseModel):
    """Toplantı gündemi"""
    items: List[str]
    duration_per_item: int  # dakika


class Meeting(BaseModel):
    """Toplantı modeli"""
    id: str
    type: str  # daily_standup, weekly_review, monthly_planning, ad_hoc
    title: str
    scheduled_time: datetime
    duration: int  # dakika
    participants: List[str]
    agenda: MeetingAgenda
    facilitator: str
    notes: List[Dict] = []
    decisions: List[Dict] = []
    action_items: List[Dict] = []
    status: str = "scheduled"  # scheduled, in_progress, completed


class MeetingSystem:
    """Toplantı sistemi"""
    
    def __init__(self):
        self.meetings: List[Meeting] = []
        self.meeting_history: List[Meeting] = []
    
    async def schedule_daily_standup(
        self, 
        department: str,
        participants: List,
        facilitator,
        scheduled_time: datetime
    ) -> Meeting:
        """Günlük standup toplantısı planla"""
        meeting = Meeting(
            id=f"standup_{department}_{datetime.now().timestamp()}",
            type="daily_standup",
            title=f"{department} Daily Standup",
            scheduled_time=scheduled_time,
            duration=15,
            participants=[p.name for p in participants],
            agenda=MeetingAgenda(
                items=[
                    "What did I do yesterday?",
                    "What will I do today?",
                    "Any blockers?"
                ],
                duration_per_item=5
            ),
            facilitator=facilitator.name
        )
        
        self.meetings.append(meeting)
        logger.info(f"📅 Toplantı planlandı: {meeting.title} - {scheduled_time}")
        return meeting
    
    async def conduct_daily_standup(
        self,
        meeting: Meeting,
        agents: List  # Type hint'i kaldırdık, runtime'da any list kabul edecek
    ) -> Dict:
        """Günlük standup toplantısını yürüt"""
        logger.info(f"\n{'='*60}")
        logger.info(f"🎤 TOPLANTI BAŞLIYOR: {meeting.title}")
        logger.info(f"🕐 Saat: {meeting.scheduled_time}")
        logger.info(f"👥 Katılımcılar: {len(agents)} kişi")
        logger.info(f"{'='*60}\n")
        
        meeting.status = "in_progress"
        updates = []
        
        for agent in agents:
            update = await agent.daily_standup_update()
            updates.append(update)
            
            logger.info(f"👤 {agent.name} ({agent.role}):")
            logger.info(f"   ✅ Dün: {', '.join(update['yesterday']) if update['yesterday'] else 'Görev yok'}")
            logger.info(f"   🎯 Bugün: {', '.join(update['today']) if update['today'] else 'Görev yok'}")
            if update['blockers']:
                logger.info(f"   ⚠️  Engeller: {', '.join(update['blockers'])}")
            print()
        
        meeting.status = "completed"
        meeting.notes = updates
        self.meeting_history.append(meeting)
        
        logger.info(f"{'='*60}")
        logger.info(f"✅ TOPLANTI TAMAMLANDI")
        logger.info(f"{'='*60}\n")
        
        return {
            "meeting_id": meeting.id,
            "type": meeting.type,
            "updates": updates,
            "duration": meeting.duration
        }
    
    async def schedule_weekly_review(
        self,
        department: str,
        participants: List,
        facilitator,
        scheduled_time: datetime
    ) -> Meeting:
        """Haftalık değerlendirme toplantısı planla"""
        meeting = Meeting(
            id=f"weekly_{department}_{datetime.now().timestamp()}",
            type="weekly_review",
            title=f"{department} Weekly Review",
            scheduled_time=scheduled_time,
            duration=60,
            participants=[p.name for p in participants],
            agenda=MeetingAgenda(
                items=[
                    "Week achievements",
                    "Metrics review",
                    "Next week planning",
                    "Cross-department updates",
                    "Challenges and solutions"
                ],
                duration_per_item=12
            ),
            facilitator=facilitator.name
        )
        
        self.meetings.append(meeting)
        return meeting
    
    async def conduct_weekly_review(
        self,
        meeting: Meeting,
        agents: List
    ) -> Dict:
        """Haftalık değerlendirme toplantısını yürüt"""
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 HAFTALIK DEĞERLENDİRME: {meeting.title}")
        logger.info(f"{'='*60}\n")
        
        meeting.status = "in_progress"
        contributions = []
        
        for agent in agents:
            contribution = await agent.generate_meeting_contribution({
                "type": "weekly_review",
                "agenda": meeting.agenda.items
            })
            contributions.append(contribution)
            
            logger.info(f"👤 {agent.name} ({agent.role}):")
            logger.info(f"   {contribution['contribution']}\n")
        
        meeting.status = "completed"
        meeting.notes = contributions
        self.meeting_history.append(meeting)
        
        logger.info(f"{'='*60}")
        logger.info(f"✅ HAFTALIK DEĞERLENDİRME TAMAMLANDI")
        logger.info(f"{'='*60}\n")
        
        return {
            "meeting_id": meeting.id,
            "type": meeting.type,
            "contributions": contributions
        }
    
    async def schedule_monthly_planning(
        self,
        participants: List,
        facilitator,
        scheduled_time: datetime
    ) -> Meeting:
        """Aylık planlama toplantısı planla"""
        meeting = Meeting(
            id=f"monthly_{datetime.now().timestamp()}",
            type="monthly_planning",
            title="Monthly Planning Meeting",
            scheduled_time=scheduled_time,
            duration=120,
            participants=[p.name for p in participants],
            agenda=MeetingAgenda(
                items=[
                    "Previous month review",
                    "Goal achievement analysis",
                    "Next month objectives",
                    "Budget review",
                    "Strategic initiatives",
                    "Resource allocation"
                ],
                duration_per_item=20
            ),
            facilitator=facilitator.name
        )
        
        self.meetings.append(meeting)
        return meeting
    
    async def conduct_monthly_planning(
        self,
        meeting: Meeting,
        agents: List
    ) -> Dict:
        """Aylık planlama toplantısını yürüt"""
        logger.info(f"\n{'='*60}")
        logger.info(f"📈 AYLIK PLANLAMA TOPLANTISI")
        logger.info(f"{'='*60}\n")
        
        meeting.status = "in_progress"
        
        # Executive contributions
        strategic_plans = []
        for agent in agents:
            if hasattr(agent, 'is_executive') and agent.is_executive:
                plan = await agent.make_strategic_decision(
                    "Gelecek ay için şirket stratejisini belirle"
                )
                strategic_plans.append(plan)
                logger.info(f"🎯 {agent.name} - Stratejik Plan:")
                logger.info(f"   {plan['decision']}\n")
        
        meeting.status = "completed"
        meeting.decisions = strategic_plans
        self.meeting_history.append(meeting)
        
        logger.info(f"{'='*60}")
        logger.info(f"✅ AYLIK PLANLAMA TAMAMLANDI")
        logger.info(f"{'='*60}\n")
        
        return {
            "meeting_id": meeting.id,
            "type": meeting.type,
            "strategic_plans": strategic_plans
        }
    
    async def schedule_ad_hoc_meeting(
        self,
        title: str,
        participants: List,
        facilitator,
        agenda_items: List[str],
        duration: int = 30
    ) -> Meeting:
        """Özel toplantı planla"""
        meeting = Meeting(
            id=f"adhoc_{datetime.now().timestamp()}",
            type="ad_hoc",
            title=title,
            scheduled_time=datetime.now(),
            duration=duration,
            participants=[p.name for p in participants],
            agenda=MeetingAgenda(
                items=agenda_items,
                duration_per_item=duration // len(agenda_items)
            ),
            facilitator=facilitator.name
        )
        
        self.meetings.append(meeting)
        return meeting
    
    async def get_meeting_summary(self, meeting_id: str) -> Optional[Dict]:
        """Toplantı özetini al"""
        for meeting in self.meeting_history:
            if meeting.id == meeting_id:
                return {
                    "id": meeting.id,
                    "type": meeting.type,
                    "title": meeting.title,
                    "date": meeting.scheduled_time,
                    "participants": meeting.participants,
                    "notes": meeting.notes,
                    "decisions": meeting.decisions,
                    "action_items": meeting.action_items
                }
        return None
    
    def get_upcoming_meetings(self) -> List[Meeting]:
        """Yaklaşan toplantıları al"""
        return [m for m in self.meetings if m.status == "scheduled"]
    
    def get_meeting_history(self, limit: int = 10) -> List[Meeting]:
        """Toplantı geçmişini al"""
        return self.meeting_history[-limit:]
