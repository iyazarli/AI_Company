"""
Dashboard - Şirket durumunu izleme ve raporlama
"""
import asyncio
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from core.company import AutonomousCompany
import time



import logging
logger = logging.getLogger(__name__)
class CompanyDashboard:
    """Şirket dashboard'u - Canlı izleme"""
    
    def __init__(self, company: AutonomousCompany):
        self.company = company
        self.console = Console()
        self.refresh_rate = 2  # saniye
    
    def create_header(self) -> Panel:
        """Dashboard başlığı"""
        text = Text()
        text.append(f"🏢 {self.company.company_name}\n", style="bold cyan")
        text.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="dim")
        
        return Panel(text, title="[bold]Otonom AI Şirket Dashboard[/bold]")
    
    def create_stats_table(self) -> Table:
        """İstatistik tablosu"""
        stats = self.company.task_manager.get_task_statistics()
        
        table = Table(title="📊 Genel İstatistikler")
        table.add_column("Metrik", style="cyan")
        table.add_column("Değer", style="green")
        
        table.add_row("Toplam Çalışan", str(len(self.company.agents)))
        table.add_row("Departman", str(len(self.company.departments)))
        table.add_row("Toplam Görev", str(stats['total_tasks']))
        table.add_row("Tamamlanan", str(stats['completed']))
        table.add_row("Devam Eden", str(stats['in_progress']))
        table.add_row("Tamamlanma Oranı", f"%{stats['completion_rate']:.1f}")
        
        return table
    
    def create_department_table(self) -> Table:
        """Departman tablosu"""
        table = Table(title="🏢 Departmanlar")
        table.add_column("Departman", style="cyan")
        table.add_column("Çalışan", justify="right", style="green")
        table.add_column("Aktif Görev", justify="right", style="yellow")
        
        for dept_name, agents in self.company.departments.items():
            active_tasks = len([
                t for t in self.company.task_manager.tasks.values()
                if t.department == dept_name and t.status == "in_progress"
            ])
            
            table.add_row(
                dept_name,
                str(len(agents)),
                str(active_tasks)
            )
        
        return table
    
    def create_task_table(self) -> Table:
        """Görev tablosu"""
        table = Table(title="📋 Son Görevler")
        table.add_column("Görev", style="cyan")
        table.add_column("Atanan", style="green")
        table.add_column("Durum", style="yellow")
        table.add_column("Öncelik", style="magenta")
        
        recent_tasks = list(self.company.task_manager.tasks.values())[-10:]
        
        for task in recent_tasks:
            status_emoji = {
                "pending": "⏳",
                "in_progress": "🔄",
                "completed": "✅",
                "blocked": "⛔"
            }.get(task.status, "❓")
            
            table.add_row(
                task.title[:40],
                task.assigned_to,
                f"{status_emoji} {task.status}",
                task.priority
            )
        
        return table
    
    def create_meeting_table(self) -> Table:
        """Toplantı tablosu"""
        table = Table(title="📅 Toplantı Geçmişi")
        table.add_column("Toplantı", style="cyan")
        table.add_column("Katılımcı", justify="right", style="green")
        table.add_column("Tarih", style="yellow")
        
        meetings = self.company.meeting_system.get_meeting_history(limit=5)
        
        for meeting in meetings:
            table.add_row(
                meeting.title,
                str(len(meeting.participants)),
                meeting.scheduled_time.strftime("%Y-%m-%d %H:%M")
            )
        
        return table
    
    def create_layout(self) -> Layout:
        """Dashboard layout"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
        )
        
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        layout["left"].split_column(
            Layout(name="stats"),
            Layout(name="departments")
        )
        
        layout["right"].split_column(
            Layout(name="tasks"),
            Layout(name="meetings")
        )
        
        # İçerikleri yerleştir
        layout["header"].update(self.create_header())
        layout["stats"].update(self.create_stats_table())
        layout["departments"].update(self.create_department_table())
        layout["tasks"].update(self.create_task_table())
        layout["meetings"].update(self.create_meeting_table())
        
        return layout
    
    async def run_live(self, duration: int = 60):
        """Canlı dashboard - Belirtilen süre boyunca"""
        with Live(self.create_layout(), refresh_per_second=1) as live:
            start_time = time.time()
            
            while time.time() - start_time < duration:
                await asyncio.sleep(self.refresh_rate)
                live.update(self.create_layout())
    
    def show_snapshot(self):
        """Anlık görüntü göster"""
        self.console.print(self.create_layout())


async def main():
    """Dashboard'u başlat"""
    from dotenv import load_dotenv
    load_dotenv()
    
    company = AutonomousCompany()
    await company.initialize()
    
    # Örnek veri oluştur
    await company.assign_tasks_to_departments()
    
    dashboard = CompanyDashboard(company)
    
    logger.info("\n📊 Dashboard açılıyor...\n")
    
    # Canlı dashboard (60 saniye)
    await dashboard.run_live(duration=60)


if __name__ == "__main__":
    asyncio.run(main())
