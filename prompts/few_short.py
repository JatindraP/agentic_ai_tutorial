"""
This file contains the few-short prompting example. 
In this example, we will create a system prompt that answers only coding-related questions 
and for other questions it will say sorry. 
We will then ask a coding-related question and a non-coding related question to see how the model responds.
"""

from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(
    api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Create a system prompt that answers only coding-related questions and for other questions it will say sorry. With some few-short prompting examples.
SYSTEM_PROMPT = """You are a helpful assistant that only answers coding-related questions. For any other questions, please say 'Sorry, I can't assist with that.' Here are some examples of how you should respond:
User: How do I reverse a string in Python?
Assistant: To reverse a string in Python, you can use slicing. Here's an example:
```python
s = "hello"
reversed_s = s[::-1]
print(reversed_s)  # Output: "olleh"
```
User: What is the capital of France?
Assistant: Sorry, I can't assist with that.
"""

# Now, let's ask a coding-related question and a non-coding related question to see how the model responds.

# Coding-related question
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":" Write a Dynamic programming solution for the Fibonacci sequence using python."}
    ]
)

#Print the response for the coding-related question
print("Response to coding-related question:")
print(response.choices[0].message.content)  

# Non-coding related question
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":" Crack a joke for me."}
    ]
)

#Print the response for the non-coding related question
print("Response to non-coding related question:")
print(response.choices[0].message.content)  