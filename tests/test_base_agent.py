"""
Unit Tests - Agent Base Tests
"""
import unittest
import logging
from datetime import datetime
from agents.base_agent import BaseAgent, Task, Message, AgentMemory

logger = logging.getLogger(__name__)

class TestBaseAgent(unittest.TestCase):
    """BaseAgent test suite"""
    
    def setUp(self):
        """Test setup"""
        self.agent = BaseAgent(
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
            title="Test Task",
            description="Testing task reception",
            priority=5
        )
        
        self.agent.receive_task(task)
        self.assertEqual(len(self.agent.memory.tasks), 1)
        self.assertEqual(self.agent.memory.tasks[0].title, "Test Task")
    
    def test_send_message(self):
        """Test message sending"""
        self.agent.send_message("recipient", "Test message")
        
        self.assertEqual(len(self.agent.memory.messages), 1)
        message = self.agent.memory.messages[0]
        self.assertEqual(message.sender, "Test Agent")
        self.assertEqual(message.recipient, "recipient")
        self.assertEqual(message.content, "Test message")
    
    def test_attend_meeting(self):
        """Test meeting attendance"""
        self.agent.attend_meeting("Daily Standup", "Stand up meeting")
        
        self.assertEqual(len(self.agent.memory.attended_meetings), 1)
        meeting = self.agent.memory.attended_meetings[0]
        self.assertEqual(meeting["title"], "Daily Standup")
    
    def test_complete_task(self):
        """Test task completion"""
        task = Task(
            title="Completable Task",
            description="Task to complete",
            priority=3
        )
        
        self.agent.receive_task(task)
        self.agent.complete_task(task, "Task completed successfully")
        
        self.assertEqual(len(self.agent.memory.completed_tasks), 1)
        completed = self.agent.memory.completed_tasks[0]
        self.assertEqual(completed.status, "completed")

class TestTask(unittest.TestCase):
    """Task model test suite"""
    
    def test_task_creation(self):
        """Test task creation with defaults"""
        task = Task(
            title="New Task",
            description="Task description"
        )
        
        self.assertEqual(task.title, "New Task")
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.priority, 5)
        self.assertIsInstance(task.created_at, datetime)
    
    def test_task_priority(self):
        """Test task priority setting"""
        task = Task(
            title="High Priority",
            description="Important task",
            priority=10
        )
        
        self.assertEqual(task.priority, 10)

class TestMessage(unittest.TestCase):
    """Message model test suite"""
    
    def test_message_creation(self):
        """Test message creation"""
        message = Message(
            sender="Alice",
            recipient="Bob",
            content="Hello Bob"
        )
        
        self.assertEqual(message.sender, "Alice")
        self.assertEqual(message.recipient, "Bob")
        self.assertEqual(message.content, "Hello Bob")
        self.assertIsInstance(message.timestamp, datetime)

if __name__ == '__main__':
    unittest.main()
