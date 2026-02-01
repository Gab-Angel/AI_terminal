from langchain_core.messages import HumanMessage
from src.graph.workflow import graph
from src.db.db_sqlite import delete_db, conn
from src.ui.console_ui import ConsoleUI

ui = ConsoleUI()

# Thread ID para manter contexto
config = {"configurable": {"thread_id": "session_1"}}

# Loop do terminal
while True:
    user_input = ui.get_input()
    
    if user_input.lower() == 'exit':
        ui.show_exit()
        conn.close()
        break
    
    elif user_input == '0':
        delete_db()
        ui.console.print("\n[bold green]✓ Histórico limpo[/]\n")
        continue
    
    # Spinner durante processamento
    spinner = ui.show_spinner("Processando")
    spinner.start()
    
    # Invoca o graph com a mensagem do usuário
    entrada = {'messages': [HumanMessage(content=user_input)]}
    result = graph.invoke(entrada, config=config)
    
    spinner.stop()

    if result.get('messages'):
        last_message = result['messages'][-1]
        metadata = getattr(last_message, 'response_metadata', {})
        total_tokens = metadata['token_usage']['total_tokens']
        total_time = metadata['token_usage']['total_time']
        llm_model = metadata['model_name']
        
        ui.show_stats(total_tokens, total_time, llm_model)