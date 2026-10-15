from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

load_dotenv()
client = OpenAI()

THRESHOLD = 0.20
TOP_K = 3

def embed(text):
    response = client.embeddings.create(model="text-embedding-3-small",input=text)
    return np.array(response.data[0].embedding)

def similarity(a,b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

KNOWLEDGE_FILES =["library_facts.txt", "library_status.txt"]

facts = []
for file_name in KNOWLEDGE_FILES:
    with open(file_name, encoding="utf-8") as file :
        for line in file:
            line = line.strip()
            if line:
                facts.append(line)

print (f"Loading {len(facts)} facts...")
fact_vectors = [embed(f) for f in facts]

def retrieve(question):
    q = embed(question)
    scores = [similarity(q,fv) for fv in fact_vectors]
    ranked = sorted(zip(scores,facts),reverse = True)
    return ranked[:TOP_K]

def answer(question,history=None):
    if history is None:
        history = []
    search_text = question
    if history:
        last_user_message = history[-2]["content"]
        search_text = last_user_message + " " + question
    results = retrieve(search_text)
    best_score = results[0][0]
    if best_score < THRESHOLD:
        return "I don't have that information. Let me pass you to a staff member.", results
    context = "\n".join(f"- {fact}" for score, fact in results)
    system_prompt = f"""You are a friendly support assistant for a library.
Answer ONLY using the facts below. Do not use any other knowledge.
If the facts do not contain the answer, reply exactly:
"I don't have that information. Let me pass you to a staff member."
Keep answers short and polite.
Facts:
{context}"""
    messages = [{"role": "system" , "content": system_prompt}]
    messages += history[-6:]
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content, results

    
if __name__ == "__main__":
    print("Library support bot ready! Type 'quit' to exit.")
    while True:
        question = input("\nYou: ")
        if question.lower() == "quit":
            break
        reply, used = answer(question)
        print("Bot:", reply)
        for score, fact in used:                    
            print(f"   [{score:.2f}] {fact}")