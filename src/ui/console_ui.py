from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from src.ui.animations import MatrixSpinner, TypingEffect
import time


class ConsoleUI:
    """Interface futurista estilo Matrix"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    BANNER = """
████████╗███████╗██████╗ ███╗   ███╗██╗██╗   ██╗███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║██║   ██║██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║██║   ██║███████╗
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║   ██║╚════██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║╚██████╔╝███████║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝ ╚═════╝ ╚══════╝
"""
    
    TOOL_ICONS = {
        'list_directory': '📂',
        'verify_if_exists': '🔍',
        'create_file': '📄',
        'create_directory': '📁',
        'read_file': '📖',
        'read_pdf': '📕',
        'get_file_info': 'ℹ️',
        'edit_file': '✏️',
        'rename': '🔄',
        'move': '➡️',
        'copy': '📋',
        'delete_file': '🗑️',
        'delete_directory': '🗂️',
        'search_file': '🔎',
    }
    
    def __init__(self):
        if not ConsoleUI._initialized:
            self.console = Console()
            self._show_banner()
            ConsoleUI._initialized = True
        elif not hasattr(self, 'console'):
            self.console = Console()
    
    def _show_banner(self):
        """Exibe banner inicial"""
        banner_text = Text(self.BANNER, style="bold green")
        subtitle = Text("◢ AGENTE DE TERMINAL v1.0 ◣", style="bold cyan")
        
        self.console.print()
        self.console.print(Align.center(banner_text))
        self.console.print(Align.center(subtitle))
        self.console.print(Align.center(Text("━" * 60, style="green")))
        self.console.print()
    
    def get_input(self) -> str:
        """Captura input do usuário"""
        self.console.print("\n[green]" + "━" * 60 + "[/]")
        self.console.print("[bold cyan]⚡ COMANDOS[/]")
        self.console.print("[green]" + "━" * 60 + "[/]")
        self.console.print("[dim green]exit[/] → Sair  |  [dim green]0[/] → Limpar histórico")
        self.console.print("[green]" + "━" * 60 + "[/]\n")
        
        return self.console.input("[bold green]▸[/] ")
    
    def show_exit(self):
        """Mensagem de saída"""
        self.console.print("\n[bold red]⚠ ENCERRANDO SISTEMA...[/]")
        time.sleep(0.5)
        self.console.print("[dim green]◢ Até logo ◣[/]\n")
    
    def show_tool_action(self, tool_name: str, *args):
        """Mostra qual ferramenta está sendo executada"""
        icon = self.TOOL_ICONS.get(tool_name, '🔧')
        args_str = ' | '.join(str(arg) for arg in args)
        self.console.print(f"\n[dim cyan]{icon} {tool_name.upper()}[/] [dim]{args_str}[/]")
    
    def show_tool_result(self, content: str):
        """Exibe resultado da ferramenta"""
        # Remove prints internos, só mostra se for relevante
        if not any(x in content for x in ['✓', '❌', '✗']):
            return
        
        color = "green" if "✓" in content else "red" if "❌" in content else "yellow"
        self.console.print(f"[{color}]{content}[/]")
    
    def show_ai_response(self, content: str):
        """Exibe resposta da IA com estilo Matrix"""
        panel = Panel(
            Text(content, style="bold green"),
            title="[bold cyan]⟪ IA RESPOSTA ⟫[/]",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    def show_stats(self, tokens: int, time_taken: float, model: str):
        """Painel de estatísticas"""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style="cyan", justify="right")
        table.add_column(style="bold green")
        
        table.add_row("TOKENS", f"{tokens:,}")
        table.add_row("TEMPO", f"{time_taken:.2f}s")
        table.add_row("MODEL", model)
        
        panel = Panel(
            table,
            title="[bold cyan]⟪ STATS ⟫[/]",
            border_style="green",
            padding=(0, 1)
        )
        self.console.print(panel)
    
    def confirm_danger(self, action: str) -> bool:
        """Confirmação para ações perigosas"""
        self.console.print(f"\n[bold yellow]⚠️  ATENÇÃO: {action}[/]")
        response = self.console.input("[bold red]Confirmar? (s/n):[/] ")
        return response.lower() == 's'
    
    def show_spinner(self, text: str = "Pensando"):
        """Retorna spinner para uso com context manager"""
        return MatrixSpinner(text)