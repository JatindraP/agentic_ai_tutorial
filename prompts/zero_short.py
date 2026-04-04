"""
    Zero-shot prompting means asking an LLM to perform a task without giving any examples.
"""

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Create a system prompt that answers only coding-related questions and for other questions it will say sorry.
SYSTEM_PROMPT = "You are a helpful assistant that only answers coding-related questions. For any other questions, please say 'Sorry, I can't assist with that.'"

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":" Write a Dynamic programming solution for the Fibonacci sequence using python."}
    ]
)

print(response.choices[0].message.content)