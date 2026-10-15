from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

messages = [
    {"role":"system","content":"You are a friendly support assistant for a library."}
]

print("Library bot ready! Type 'quit' to exit.")
while True:
    user_text = input("You: ")
    if user_text.lower() == "quit":
        break
    messages.append({"role":"user","content":user_text})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )
    reply = response.choices[0].message.content
    messages.append({"role":"assistant","content":reply})
    print("Bot:",reply)
    print("[tokens sent:",response.usage.prompt_tokens,"]")
    