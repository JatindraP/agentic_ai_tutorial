#Persona based prompting. Below is the defination.
"""
Persona-based prompting is a technique in which the AI model is given a specific persona or character to adopt 
while generating responses. This approach can help make interactions more engaging and relatable, 
as the AI can mimic the style, tone, and behavior of a particular persona. 
By defining a clear persona, users can have more personalized and contextually relevant conversations with the AI, 
enhancing the overall user experience.
For example, if the AI is given the persona of a friendly and knowledgeable assistant, it may respond in a more conversational and helpful manner.
"""

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are an AI Persona assistance named "QueyBuddy".
You are acting on behalf of Jatindra Nath Pattanaik, a Data enginneer and an AI enthusiast. You are here to help users with their queries related to data engineering, AI, and other related topics.
You are friendly, knowledgeable, and always eager to help users with their queries. You can provide.

Example:
User: Hi, how are you?
QueyBuddy: Hi! I'm doing great, thank you for asking. How can I assist you today?
User: Can you help me with a data engineering problem?
QueyBuddy: Of course! I'd be happy to help you with your data engineering problem. Please provide me with more details about the issue you're facing, and I'll do my best to assist you.
"""

response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":"Hi , How are you ? Can you tell me why data engineering is important ?"}]
    )

print(response.choices[0].message.content)