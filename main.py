from rich.console import Console
from langchain_core.messages import HumanMessage
from src.graph.workflow import graph
from src.db.db_sqlite import delete_db
console = Console()

# Thread ID para manter contexto
config = {"configurable": {"thread_id": "session_1"}}

# Loop do terminal
while True:
    user_input = console.input(
        "\n[bold cyan]" + "="*50 + "[/]\n"
        "[bold yellow]              COMANDOS DISPONÍVEIS[/]\n"
        "[bold cyan]" + "="*50 + "[/]\n"
        "[dim]exit[/]  → Sair do programa\n"
        "[dim]0[/]     → Deletar histórico\n"
        "[bold cyan]" + "="*50 + "[/]\n\n"
        "[bold green]Você:[/] "
    )
    
    if user_input.lower() == 'exit':
        console.print("\n[bold red]Encerrando...[/]")
        break
    
    elif user_input == '0':
        delete_db()        
        continue
    
    # Invoca o graph com a mensagem do usuário
    entrada = {'messages': [HumanMessage(content=user_input)]}
    result = graph.invoke(entrada, config=config)
    
    # Pega e exibe a resposta da IA
    if result.get('messages'):
        ai_response = result["messages"][-1].content
        console.print(f"\n[bold blue]IA:[/] {ai_response}\n")