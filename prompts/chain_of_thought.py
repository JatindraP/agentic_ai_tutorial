# Chain of Thought Prompt
#Defination of the Chain of Thought Prompt

"""
The Chain of Thought Prompt is a technique used in natural language processing (NLP) 
to enhance the reasoning capabilities of language models. It involves breaking down complex problems 
into smaller, more manageable steps, 
allowing the model to generate intermediate reasoning before arriving at a final answer. 
This approach can improve the model's ability to solve multi-step problems 
and provide more accurate and coherent responses.


The Chain of Thought Prompt typically consists of a series of prompts 
that guide the model through the reasoning process. 
Each prompt is designed to elicit specific information or encourage the model 
to think critically about the problem at hand. 
For example, a Chain of Thought Prompt for solving a math problem might include prompts 
like "What is the first step to solve this problem?" or "What information do we need to find the solution?
"""

import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI()

print("\n\n\n")
print("🚀 Welcome to the Chain of Thought Prompting Example! 🚀")

SYSTEM_PROMPT = """
Yoe are a AI assistance in resolving the user query using the chauin of thought prompting technique.
You work on START -> PLAN -> OUTPUT steps.
Yoe need to first PLAN what needs to be done. The plan can be in multiple steps.
Once you think enough PLAN has been done, finally you can give the OUTPUT.

Rules:
 - Strictly follow the given JSON output format.
 - Only run one step at a time.
 - The sequence of steps is START(where user gives an input) -> PLAN(Than can be multiple times) -> OUTPUT(Which is going to be displayed to the user).

 Output JSON Format:
 {
    "step": "START/PLAN/OUTPUT",
    "content": "output of each step in the form of text. PLAN step will be multiple times and each PLAN step should be in the form of text. The final OUTPUT step will be in the form of text that will be displayed to the user."
 }

 Example:
 Q: Can you solve the math problem 2+3*5/10 ?
    A:
    {
        "step": "START",
        "content": "The user has asked to solve the math problem 2+3*5/10."
    }
    {
        "step": "PLAN",
        "content": "First, we need to follow the order of operations (PEMDAS/BODMAS). We will start with the parentheses, then exponents, followed by multiplication and division from left to right, and finally addition and subtraction from left to right."
    }
    {
        "step": "PLAN",
        "content": "Next, we will perform the multiplication and division first. So we will calculate 3*5 which gives us 15, and then we will divide that by 10 which gives us 1.5."
    }
    {
        "step": "PLAN",
        "content": "Finally, we will add the result of the multiplication and division to 2. So we will calculate 2 + 1.5 which gives us 3.5."
    }
    {
        "step": "OUTPUT",
        "content": "The answer to the math problem 2+3*5/10 is 3.5."
    }
"""

message_hist = [
    {"role":"system","content":SYSTEM_PROMPT},
]
user_query = input("🙋‍♂️ Hey, Ask me anything ...‼️\n👉")
message_hist.append({"role":"user","content":user_query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=message_hist
    )
    raw_result = response.choices[0].message.content
    message_hist.append({"role":"assistant","content":raw_result})
    parsed_result = json.loads(raw_result)
    print("\n")
    if parsed_result.get("step") == "START":
        print(f"💫 {parsed_result.get('content')}")
        print("🤔 Let me think step by step ...")
        continue
    elif parsed_result.get("step") == "PLAN":
        print(f"🧠 {parsed_result.get('content')}")
    elif parsed_result.get("step") == "OUTPUT":
        print(f"🤖 {parsed_result.get('content')}")
        print("✅ All steps completed.")
        print("😇")
        break
    

print("\n\n\n")