"""
Agent Factory - YAML config'den ajanları oluştur
"""
import yaml
import logging
from typing import Dict, List
from agents.ai_agent import AIAgent, ManagerAgent, ExecutiveAgent
from systems.ai_provider import get_ai_provider, AIProvider

logger = logging.getLogger(__name__)


class AgentFactory:
    """YAML config'den AI ajanları oluşturur"""
    
    def __init__(self, config_path: str = "config/company_config.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.agents: Dict[str, AIAgent] = {}
        self.departments: Dict[str, List[AIAgent]] = {}
    
    def create_all_agents(self) -> Dict[str, AIAgent]:
        """Tüm ajanları oluştur"""
        departments_config = self.config.get('departments', {})
        
        # Technology Department
        tech_dept = departments_config.get('technology', {})
        self._create_tech_agents(tech_dept)
        
        # Marketing Department
        marketing_dept = departments_config.get('marketing', {})
        self._create_department_agents('marketing', marketing_dept)
        
        # Business Development
        bizdev_dept = departments_config.get('business_development', {})
        self._create_department_agents('business_development', bizdev_dept)
        
        # Finance
        finance_dept = departments_config.get('finance', {})
        self._create_department_agents('finance', finance_dept)
        
        # HR
        hr_dept = departments_config.get('human_resources', {})
        self._create_department_agents('human_resources', hr_dept)
        
        # Customer Service
        cs_dept = departments_config.get('customer_service', {})
        self._create_department_agents('customer_service', cs_dept)
        
        # Management
        mgmt_dept = departments_config.get('management', {})
        self._create_management_agents(mgmt_dept)
        
        # Legal
        legal_dept = departments_config.get('legal', {})
        self._create_department_agents('legal', legal_dept)
        
        logger.info(f"✅ Toplam {len(self.agents)} AI çalışan oluşturuldu")
        return self.agents
    
    def _create_tech_agents(self, tech_config: Dict):
        """Teknoloji departmanı ajanlarını oluştur"""
        teams = tech_config.get('teams', {})
        
        for team_name, members in teams.items():
            for member in members:
                agent = AIAgent(
                    name=member['name'],
                    role=member['role'],
                    department=f"Technology/{team_name}",
                    skills=member['skills'],
                    ai_provider_manager=self.ai_provider_manager
                )
                self.agents[member['name']] = agent
                
                dept_key = 'technology'
                if dept_key not in self.departments:
                    self.departments[dept_key] = []
                self.departments[dept_key].append(agent)
    
    def _create_department_agents(self, dept_name: str, dept_config: Dict):
        """Genel departman ajanlarını oluştur"""
        team = dept_config.get('team', [])
        manager_name = dept_config.get('manager')
        
        team_members = []
        
        for member in team:
            # Manager ise ManagerAgent, değilse AIAgent oluştur
            if 'Manager' in member['role'] or 'Director' in member['role'] or member['role'] == 'CFO':
                agent = ManagerAgent(
                    name=member['name'],
                    role=member['role'],
                    department=dept_name,
                    skills=member['skills'],
                    team_members=[],  # Sonra doldurulacak
                    ai_provider_manager=self.ai_provider_manager
                )
            else:
                agent = AIAgent(
                    name=member['name'],
                    role=member['role'],
                    department=dept_name,
                    skills=member['skills'],
                    ai_provider_manager=self.ai_provider_manager
                )
                team_members.append(member['name'])
            
            self.agents[member['name']] = agent
            
            if dept_name not in self.departments:
                self.departments[dept_name] = []
            self.departments[dept_name].append(agent)
        
        # Manager'a takım üyelerini ata
        for member in team:
            if 'Manager' in member['role'] or 'Director' in member['role']:
                if isinstance(self.agents[member['name']], ManagerAgent):
                    self.agents[member['name']].team_members = team_members
    
    def _create_management_agents(self, mgmt_config: Dict):
        """Yönetim kadrosu ajanlarını oluştur"""
        team = mgmt_config.get('team', [])
        
        for member in team:
            # CEO ve C-level için ExecutiveAgent
            if member['role'] in ['CEO', 'CTO', 'CFO', 'CMO', 'COO']:
                agent = ExecutiveAgent(
                    name=member['name'],
                    role=member['role'],
                    department='management',
                    skills=member['skills'],
                    ai_provider_manager=self.ai_provider_manager
                )
            # Project Manager vb için ManagerAgent
            elif 'Manager' in member['role']:
                agent = ManagerAgent(
                    name=member['name'],
                    role=member['role'],
                    department='management',
                    skills=member['skills'],
                    ai_provider_manager=self.ai_provider_manager
                )
            else:
                agent = AIAgent(
                    name=member['name'],
                    role=member['role'],
                    department='management',
                    skills=member['skills'],
                    ai_provider_manager=self.ai_provider_manager
                )
            
            self.agents[member['name']] = agent
            
            if 'management' not in self.departments:
                self.departments['management'] = []
            self.departments['management'].append(agent)
    
    def get_agent(self, name: str) -> AIAgent:
        """İsme göre ajan al"""
        return self.agents.get(name)
    
    def get_department_agents(self, department: str) -> List[AIAgent]:
        """Departmana göre ajanları al"""
        return self.departments.get(department, [])
    
    def get_all_agents(self) -> List[AIAgent]:
        """Tüm ajanları al"""
        return list(self.agents.values())
    
    def get_managers(self) -> List[ManagerAgent]:
        """Tüm yöneticileri al"""
        return [a for a in self.agents.values() if isinstance(a, ManagerAgent)]
    
    def get_executives(self) -> List[ExecutiveAgent]:
        """Tüm üst yönetimi al"""
        return [a for a in self.agents.values() if isinstance(a, ExecutiveAgent)]
