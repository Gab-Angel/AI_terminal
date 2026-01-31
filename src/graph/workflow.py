from src.graph.nodes import Nodes
from langgraph.graph import END, StateGraph
from src.graph.state import State
from src.db.db_sqlite import memory

workflow = StateGraph(State)

workflow.add_node('ai_main', Nodes.node_ai_main)
workflow.add_node('execute_tools', Nodes.node_execute_tools)
workflow.add_node('response', Nodes.node_response_in_terminal)

workflow.set_entry_point('ai_main')

workflow.add_conditional_edges(
    'ai_main',
    Nodes.node_use_tools,
    {'yes': 'execute_tools', 'no': 'response'},
)

workflow.add_edge('execute_tools', 'ai_main')
workflow.add_edge('response', END)

graph = workflow.compile(checkpointer=memory)