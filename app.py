import chainlit as cl
from rag_bot import answer

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="Hi! I'm the library assistant. Ask me about our books, borrowing rules or opening hours."
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history")

    reply,used = await cl.make_async(answer)(message.content,history)

    history.append({"role": "user", "content": message.content})
    history.append({"role": "assistant", "content": reply})
    cl.user_session.set("history", history)

    await cl.Message(content=reply).send()