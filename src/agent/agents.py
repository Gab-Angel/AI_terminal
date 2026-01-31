import os
from src.prompts.get_prompt import get_prompt
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

load_dotenv()

# CONEXÃO COM A GROQ
llm_groq = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model_name='openai/gpt-oss-120b',
    temperature=0,
)

# MODELS
# openai/gpt-oss-120b
# llama-3.3-70b-versatile


PROMPT_AI = os.getenv('PROMPT_MAIN')
prompt_main = get_prompt(prompt_name=PROMPT_AI)


def agent_main(state, prompt_ia: str, llm_model):
    
    prompt_ia = prompt_main

    message_history = state['messages']
    
    system_prompt = SystemMessage(content=prompt_ia)
    
    messages = [system_prompt] + message_history
    
    response = llm_model.invoke(messages)
    
    return {'messages': [response]}