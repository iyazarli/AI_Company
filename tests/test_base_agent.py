"""
Unit Tests - Agent Base Tests
"""
import unittest
import logging
from datetime import datetime
from agents.base_agent import BaseAgent, Task, Message, AgentMemory

logger = logging.getLogger(__name__)

# Mock concrete agent for testing
class MockAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing"""
    
    async def execute_task(self, task: Task) -> str:
        """Mock task execution"""
        return f"Executed: {task.title}"
    
    async def generate_meeting_contribution(self, meeting_info: dict) -> dict:
        """Mock meeting contribution"""
        return {
            "agent": self.name,
            "contribution": f"My thoughts on {meeting_info.get('title', 'meeting')}"
        }

class TestBaseAgent(unittest.TestCase):
    """BaseAgent test suite"""
    
    def setUp(self):
        """Test setup"""
        self.agent = MockAgent(
            name="Test Agent",
            role="tester",
            department="qa",
            skills=["testing", "debugging"]
        )
    
    def test_agent_creation(self):
        """Test agent initialization"""
        self.assertEqual(self.agent.name, "Test Agent")
        self.assertEqual(self.agent.role, "tester")
        self.assertEqual(self.agent.department, "qa")
        self.assertIn("testing", self.agent.skills)
    
    def test_receive_task(self):
        """Test task reception"""
        task = Task(
            id="test-task-1",
            title="Test Task",
            description="Testing task reception",
            priority="medium",
            assigned_to="Test Agent",
            assigned_by="Manager",
            department="qa"
        )
        
        # receive_task is async
        import asyncio
        result = asyncio.run(self.agent.receive_task(task))
        self.assertTrue(result)
        self.assertEqual(len(self.agent.memory.tasks_active), 1)
    
    def test_send_message(self):
        """Test message sending"""
        import asyncio
        message = asyncio.run(self.agent.send_message("recipient", "Test Subject", "Test message"))
        
        self.assertIsNotNone(message)
        self.assertEqual(len(self.agent.memory.messages_sent), 1)
        self.assertEqual(message.from_agent, "Test Agent")
        self.assertEqual(message.to_agent, "recipient")
        self.assertEqual(message.content, "Test message")
    
    def test_attend_meeting(self):
        """Test meeting attendance"""
        import asyncio
        meeting_info = {"title": "Daily Standup", "description": "Stand up meeting"}
        asyncio.run(self.agent.attend_meeting(meeting_info))
        
        self.assertEqual(len(self.agent.memory.meetings_attended), 1)
    
    def test_complete_task(self):
        """Test task completion"""
        import asyncio
        task = Task(
            id="test-task-2",
            title="Completable Task",
            description="Task to complete",
            priority="high",
            assigned_to="Test Agent",
            assigned_by="Manager",
            department="qa"
        )
        
        asyncio.run(self.agent.receive_task(task))
        asyncio.run(self.agent.complete_task("test-task-2", "Task completed successfully"))
        
        self.assertEqual(len(self.agent.memory.tasks_completed), 1)
        completed = self.agent.memory.tasks_completed[0]
        self.assertEqual(completed.status, "completed")

class TestTask(unittest.TestCase):
    """Task model test suite"""
    
    def test_task_creation(self):
        """Test task creation with all required fields"""
        task = Task(
            id="task-001",
            title="New Task",
            description="Task description",
            assigned_to="Developer",
            assigned_by="Manager",
            department="technology"
        )
        
        self.assertEqual(task.title, "New Task")
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.priority, "medium")  # default value
        self.assertIsInstance(task.created_at, datetime)
    
    def test_task_priority(self):
        """Test task priority setting"""
        task = Task(
            id="task-002",
            title="High Priority",
            description="Important task",
            priority="critical",
            assigned_to="Developer",
            assigned_by="Manager",
            department="technology"
        )
        
        self.assertEqual(task.priority, "critical")

class TestMessage(unittest.TestCase):
    """Message model test suite"""
    
    def test_message_creation(self):
        """Test message creation with all required fields"""
        message = Message(
            id="msg-001",
            from_agent="Alice",
            to_agent="Bob",
            subject="Hello",
            content="Hello Bob"
        )
        
        self.assertEqual(message.from_agent, "Alice")
        self.assertEqual(message.to_agent, "Bob")
        self.assertEqual(message.content, "Hello Bob")
        self.assertIsInstance(message.timestamp, datetime)

if __name__ == '__main__':
    unittest.main()
