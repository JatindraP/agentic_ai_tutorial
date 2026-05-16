from openai import OpenAI
from dotenv import load_dotenv
import requests
from pydantic import BaseModel,Field
from typing import Optional
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
Yoe are a AI assistance in resolving the user query using the chauin of thought prompting technique.
You work on START -> PLAN -> OUTPUT steps.
Yoe need to first PLAN what needs to be done. The plan can be in multiple steps.
Once you think enough PLAN has been done, finally you can give the OUTPUT.
You can also call a tool if required from the list of available tools.
For every tool call wait fro observe step which is the output of the tool call.

Available Tools:
1. get_weather(city: str) -> str : This tool takes a city name as input and returns the current weather information for that city.

Rules:
 - Strictly follow the given JSON output format.
 - Only run one step at a time.
 - The sequence of steps is START(where user gives an input) -> PLAN(Than can be multiple times) -> OUTPUT(Which is going to be displayed to the user).

 Output JSON Format:
 {
    "step": "START/PLAN/OUTPUT/"TOOL",
    "content": "output of each step in the form of text. PLAN step will be multiple times and each PLAN step should be in the form of text. The final OUTPUT step will be in the form of text that will be displayed to the user."
 }

 Example1:
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

Example2:
 Q: What is the weather in London?
    A:
    {
        "step": "START",
        "content": "The user wants to know the weather in London."
    }
    {
        "step": "PLAN",
        "content": "Let's see if we have a tool to get the weather information. Yes, we have a tool called get_weather(city: str) that can be used to get the current weather information for a given city."
    }
    {
        "step": "PLAN",
        "content": "Next, we will call the get_weather tool with the city name 'London'."
    }
    {
        "step": "TOOL",
        "tool_name": "get_weather",
        "input": "London",
        "content": "Calling get_weather with city 'London'."
    }
    {
        "step": "OBTAINED_TOOL_RESULT",
        "content": "The weather in London 15°C."
    }
    {
        "step": "OUTPUT",
        "content": "The weather in London is currently sunny with a temperature of 15°C."
    }
"""

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"🌤️ {response.text.strip()}"
    return "🌤️ Weather information not available."

available_tools = {
    "get_weather": get_weather
}

class LlmOutputFormat(BaseModel):
    step: str = Field(..., description="The step in the process. It can be START, PLAN, TOOL, OBTAINED_TOOL_RESULT, or OUTPUT.")
    content: Optional[str] = Field(None, description="The content of the output")
    tool_name: Optional[str] = Field(None, description="The name of the tool to be used if step is TOOL")
    input: Optional[str] = Field(None, description="The input for the tool if step is TOOL")

def main():
    message_hist = [
    {"role":"system","content":SYSTEM_PROMPT},
    ]
    while True:
        user_query = input("👉 ")
        if user_query.lower() in ["exit", "quit", "stop", "goodbye", "bye", "see you", "later",'']:
            print("👋 Goodbye!")
            break
        message_hist.append({"role": "user", "content": user_query})
        while True:
            response = client.chat.completions.parse(
                model="gpt-4o",
                response_format=LlmOutputFormat,
                messages=message_hist
            )

            raw_result = response.choices[0].message.content
            message_hist.append({"role":"assistant","content":raw_result})
            parsed_result = response.choices[0].message.parsed
            print("\n")
            if parsed_result.step == "START":
                print(f"💫 {parsed_result.content}")
                print("🤖 Let me think step by step ...")
                continue
            elif parsed_result.step == "PLAN":
                print(f"🧠 {parsed_result.content}")

            elif parsed_result.step == "TOOL":
                tool_name = parsed_result.tool_name
                tool_input = parsed_result.input
                tool_result = available_tools[tool_name](tool_input)
                message_hist.append({"role": "developer", "content": json.dumps(
                    {
                        "step": "OBTAINED_TOOL_RESULT",
                        "tool_name": tool_name,
                        "input": tool_input,
                        "content": tool_result
                    }
                )})
                print(f"🛠️ {tool_name} tool is used with input '{tool_input}': {tool_result}")
                continue

            elif parsed_result.step == "OUTPUT":
                print(f"🤖 {parsed_result.content}")
                print("✅ All steps completed.")
                print("😇")
                break
    


if __name__ == "__main__":
    main()
