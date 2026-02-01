from rich.console import Console
from langchain_core.messages import HumanMessage
from src.graph.workflow import graph
from src.db.db_sqlite import delete_db, conn
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
        conn.close()
        break
    
    elif user_input == '0':
        delete_db()        
        continue
    
    # Invoca o graph com a mensagem do usuário
    entrada = {'messages': [HumanMessage(content=user_input)]}
    result = graph.invoke(entrada, config=config)

    if result.get('messages'):
        last_message = result['messages'][-1]
        metadata = getattr(last_message, 'response_metadata', {})
        total_tokens = metadata['token_usage']['total_tokens']
        total_time = metadata['token_usage']['total_time']
        llm_model = metadata['model_name']

    console.print(
        f'\n{"="*50}\n\n'
        f'TOTAL DE TOKENS: [bold yellow]{total_tokens}[/]\n'
        f'TOTAL DE TEMPO: [bold yellow]{total_time}[/]\n'
        f'MODEL: [bold yellow]{llm_model}[/]'
    )
    