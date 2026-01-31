from langchain.tools import tool
from dotenv import load_dotenv
import os
from langgraph.prebuilt import ToolNode
from src.agent.agents import llm_groq

class Tools:
    @tool(description='')
    def list_directory():
        ...

    @tool(description='')
    def verify_if_exists():
        ...
        
    @tool(description='')
    def create_file():
        ...
    
    @tool(description='')
    def create_directory():
        ...
    
    @tool(description='')
    def read_file():
        ...
    
    @tool(description='')
    def get_file_info():
        ...
    
    @tool(description='')
    def count_lines():
        ...
    
    @tool(description='')
    def edit_file():
        ...
    
    @tool(description='')
    def rename():
        ...
    
    @tool(description='')
    def move():
        ...
    
    @tool(description='')
    def copy():
        ...
    
    @tool(description='')
    def delete_file():
        ...
    
    @tool(description='')
    def delete_directory():
        ...
    
    @tool(description='')
    def search_file():
        ...

    tools_main = [
        list_directory,
        verify_if_exists,
        create_file,
        create_directory,
        read_file,
        get_file_info,
        count_lines,
        edit_file,
        rename,
        move,
        copy,
        delete_file,
        delete_directory,
        search_file,
    ]


    tool_node = ToolNode(tools_main)

    llm_with_tools = llm_groq.bind_tools(tools_main)