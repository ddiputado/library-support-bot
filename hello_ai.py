from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response =client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
    {"role": "system", "content": "You are a helpful assistant for a library."},
    {"role": "user","content":"Hi! What can i help you with ?"},

    ],
    temperature=1.5,
)
print(response.choices[0].message.content)
print(response.usage)