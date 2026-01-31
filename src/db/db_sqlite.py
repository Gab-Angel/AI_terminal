from rich.console import Console
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)

console = Console()

def delete_db():
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM checkpoints")
        conn.commit()
        console.print("[yellow]✓ Histórico completo deletado![/]")
    except Exception as e:
        console.print(f"[red]Erro ao deletar histórico: {e}[/]")