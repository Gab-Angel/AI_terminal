from src.prompts.get_prompt import get_prompt
import os
from dotenv import load_dotenv

load_dotenv()

PROMPT = os.getenv('PROMPT_MAIN')
print(PROMPT)
prompt = get_prompt(prompt_name=PROMPT)

print(prompt)