"""
    A system prompt is:
        👉 A hidden instruction given to an AI model that defines how it should behave, think, and respond
    
    🔍 Simple Explanation

        If AI were a human:

            User prompt = your question
            System prompt = personality + rules + job description
"""

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content":"You are a Mathematics expert ans you can answer to the questions related to Mathematics only.Other than mathematics question you have to say Sorry."},
        {"role":"user","content":" Calculate the valu of 'x' from the equation (x+x)/x = 1."}
    ]
)

print(response.choices[0].message.content)