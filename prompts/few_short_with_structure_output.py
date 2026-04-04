"""
This file contains the few-short prompting example. 
In this example, we will create a system prompt that answers only coding-related questions 
and for other questions it will say sorry. 
We will then ask a coding-related question and a non-coding related question to see how the model responds.
We will ask the model to properly structure the output by using JSON format.
"""

from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(
    api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Create a system prompt that answers only coding-related questions and for other questions it will say sorry. With some few-short prompting examples and also asking the model to structure the output in JSON format.
SYSTEM_PROMPT = """You are a helpful assistant that only answers coding-related questions. For any other questions, please say 'Sorry, I can't assist with that.' 

Rules:
1. Always respond in JSON format with the following structure:
{
    "code": "Only the solution code in stringformat" Or None,
    "isCoadingQuestion": True or False
}

Here are some examples of how you should respond:
User: How do I reverse a string in Python?
Assistant: {
    "code": "s = 'hello'\nreversed_s = s[::-1]\nprint(reversed_s)  # Output: 'olleh'",
    "isCoadingQuestion": true
}
User: What is the capital of France?
Assistant: {
    "code": null,
    "isCoadingQuestion": false
}
"""

# Now, let's ask a coding-related question and a non-coding related question to see how the model responds.

# Coding-related question
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": " Write a Dynamic programming solution for the Fibonacci number using python."}
    ]
)
# Print the response for the coding-related question
print("Response to coding-related question:")
print(response.choices[0].message.content)

# Non-coding related question
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Translate 'Hello, how are you?' to Spanish."}
    ]
)
# Print the response for the non-coding related question
print("Response to non-coding related question:")
print(response.choices[0].message.content)

