from google import genai

client = genai.Client(
    api_key="XXXXXXXXXXXXXXXXXXXX"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",contents="Hey There!"
)

print(response.text)