from src.graph.state import State
from src.agent.agents import agent_main
from src.graph.tools import Tools
from rich.console import Console

console = Console()


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
            print('🔍 Decisão: Chamar ferramentas.')
            return 'yes'
        else:
            print('✅ Decisão: Finalizar e responder.')
            return 'no'

    @staticmethod
    def node_execute_tools(state: State):
        print('🛠️ Executando ferramentas...')
        last_message = state['messages'][-1]

        response = Tools.tool_node.invoke({'messages': [last_message]})

        for msg in response['messages']:
            print(f'🔧 Resultado da ferramenta: {msg.content}')

        return {'messages': response['messages']} 
    
    @staticmethod
    def node_response_in_terminal(state: State):
        last_message = state['messages'][-1]
        
        console.print(f"\n[bold blue]IA:[/] {last_message.content}\n")
        
        return state
        