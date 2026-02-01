from src.graph.state import State
from src.agent.agents import agent_main
from src.graph.tools import Tools
from src.ui.console_ui import ConsoleUI
from langchain_core.messages import ToolMessage

ui = ConsoleUI()


class Nodes:
    @staticmethod
    def node_ai_main(state: State):
        return agent_main(
            state=state,
            prompt_ia='',
            llm_model=Tools.llm_with_tools
        )
    
    @staticmethod
    def node_use_tools(state: State) -> str:
        last_message = state['messages'][-1]

        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            ui.console.print('[dim cyan]🔍 Decisão: Chamar ferramentas[/]')
            return 'yes'
        else:
            ui.console.print('[dim green]✅ Decisão: Finalizar[/]')
            return 'no'

    @staticmethod
    def node_execute_tools(state: State):
        last_message = state['messages'][-1]
        
        # Verifica se é operação perigosa
        for tool_call in last_message.tool_calls:
            if tool_call['name'] in ['delete_directory', 'delete_file']:
                if not ui.confirm_danger(f"Deletar: {tool_call['args']}"):
                    return {'messages': [ToolMessage(
                        content="❌ Operação cancelada pelo usuário",
                        tool_call_id=tool_call['id']
                    )]}
        
        response = Tools.tool_node.invoke({'messages': [last_message]})
        
        for msg in response['messages']:
            ui.show_tool_result(msg.content)
        
        return {'messages': response['messages']} 
    
    @staticmethod
    def node_response_in_terminal(state: State):
        last_message = state['messages'][-1]
        ui.show_ai_response(last_message.content)
        return state