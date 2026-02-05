"""
Messaging System - Departmanlar arası mesajlaşma sistemi
"""
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel
import asyncio
from agents.base_agent import Message
from agents.ai_agent import AIAgent


class Channel(BaseModel):
    """Mesajlaşma kanalı"""
    id: str
    name: str
    type: str  # department, project, direct, general
    members: List[str]
    messages: List[Message] = []
    created_at: datetime = datetime.now()


class MessagingSystem:
    """İletişim ve mesajlaşma sistemi"""
    
    def __init__(self):
        self.channels: Dict[str, Channel] = {}
        self.direct_messages: List[Message] = []
        self.agents: Dict[str, AIAgent] = {}
    
    def register_agent(self, agent: AIAgent):
        """Agentı sisteme kaydet"""
        self.agents[agent.name] = agent
    
    def create_channel(
        self,
        name: str,
        channel_type: str,
        members: List[str]
    ) -> Channel:
        """Yeni kanal oluştur"""
        channel = Channel(
            id=f"channel_{len(self.channels)}",
            name=name,
            type=channel_type,
            members=members
        )
        
        self.channels[channel.id] = channel
        print(f"📢 Yeni kanal oluşturuldu: {name}")
        return channel
    
    async def send_message(
        self,
        from_agent: AIAgent,
        to_agent: str,
        subject: str,
        content: str
    ) -> Message:
        """Direkt mesaj gönder"""
        message = await from_agent.send_message(to_agent, subject, content)
        
        # Alıcıya ilet
        if to_agent in self.agents:
            recipient = self.agents[to_agent]
            await recipient.receive_message(message)
        
        self.direct_messages.append(message)
        return message
    
    async def send_channel_message(
        self,
        channel_id: str,
        from_agent: AIAgent,
        content: str
    ) -> Optional[Message]:
        """Kanala mesaj gönder"""
        if channel_id not in self.channels:
            return None
        
        channel = self.channels[channel_id]
        
        message = Message(
            id=f"msg_{datetime.now().timestamp()}",
            from_agent=from_agent.name,
            to_agent=channel.name,
            subject=f"Message in {channel.name}",
            content=content
        )
        
        channel.messages.append(message)
        
        # Kanal üyelerine bildir
        for member_name in channel.members:
            if member_name in self.agents and member_name != from_agent.name:
                await self.agents[member_name].receive_message(message)
        
        return message
    
    async def broadcast_message(
        self,
        from_agent: AIAgent,
        subject: str,
        content: str,
        recipients: List[str] = None
    ):
        """Toplu mesaj gönder"""
        if recipients is None:
            recipients = list(self.agents.keys())
        
        for recipient_name in recipients:
            if recipient_name != from_agent.name:
                await self.send_message(from_agent, recipient_name, subject, content)
        
        print(f"📣 {from_agent.name} toplu mesaj gönderdi: {subject}")
    
    def get_channel_messages(self, channel_id: str) -> List[Message]:
        """Kanal mesajlarını al"""
        if channel_id in self.channels:
            return self.channels[channel_id].messages
        return []
    
    def get_unread_messages(self, agent_name: str) -> List[Message]:
        """Okunmamış mesajları al"""
        if agent_name in self.agents:
            agent = self.agents[agent_name]
            return [m for m in agent.memory.messages_received if not m.read]
        return []
    
    def create_department_channels(self, departments: Dict[str, List[AIAgent]]):
        """Departman kanallarını oluştur"""
        for dept_name, agents in departments.items():
            self.create_channel(
                name=f"#{dept_name}",
                channel_type="department",
                members=[a.name for a in agents]
            )
    
    def create_project_channel(self, project_name: str, team_members: List[str]) -> Channel:
        """Proje kanalı oluştur"""
        return self.create_channel(
            name=f"#{project_name}",
            channel_type="project",
            members=team_members
        )


class CollaborationSystem:
    """İş birliği ve koordinasyon sistemi"""
    
    def __init__(self, messaging: MessagingSystem):
        self.messaging = messaging
        self.active_collaborations: List[Dict] = []
    
    async def initiate_collaboration(
        self,
        initiator: AIAgent,
        collaborator_name: str,
        topic: str,
        context: str
    ) -> Dict:
        """İş birliği başlat"""
        print(f"\n🤝 İş birliği başlatılıyor:")
        print(f"   Başlatan: {initiator.name}")
        print(f"   İş birlikçi: {collaborator_name}")
        print(f"   Konu: {topic}\n")
        
        # Başlatıcının planı
        initiator_plan = await initiator.collaborate(collaborator_name, topic)
        
        # Mesaj gönder
        await self.messaging.send_message(
            initiator,
            collaborator_name,
            f"Collaboration: {topic}",
            f"{context}\n\n{initiator_plan}"
        )
        
        collaboration = {
            "id": f"collab_{datetime.now().timestamp()}",
            "initiator": initiator.name,
            "collaborator": collaborator_name,
            "topic": topic,
            "started_at": datetime.now(),
            "status": "active"
        }
        
        self.active_collaborations.append(collaboration)
        return collaboration
    
    async def cross_department_meeting(
        self,
        departments: List[str],
        topic: str,
        agents: Dict[str, AIAgent]
    ) -> Dict:
        """Departmanlar arası toplantı"""
        print(f"\n🔄 Departmanlar Arası Toplantı:")
        print(f"   Konu: {topic}")
        print(f"   Departmanlar: {', '.join(departments)}\n")
        
        participants = [
            agent for agent in agents.values()
            if any(dept in agent.department for dept in departments)
        ]
        
        contributions = []
        for agent in participants[:5]:  # İlk 5 katılımcı
            contribution = await agent.generate_meeting_contribution({
                "type": "cross_department",
                "topic": topic,
                "agenda": [topic]
            })
            contributions.append(contribution)
            print(f"💬 {agent.name}: {contribution['contribution'][:100]}...\n")
        
        return {
            "topic": topic,
            "departments": departments,
            "contributions": contributions,
            "timestamp": datetime.now()
        }
