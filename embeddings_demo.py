from openai import OpenAI
from dotenv import load_dotenv
import numpy as np 

load_dotenv()
client = OpenAI()

def embed(text):
    response = client.embeddings.create(model="text-embedding-3-small",input=text)
    return np.array(response.data[0].embedding)

v = embed("Hello, world!")
print("How many numbers:", len(v))
print("The first 5:", v[:5])
def similarity(a,b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

facts = [
    "Members can borrow up to 3 books at the same time.",
    "The library is open Monday to Friday from 9:00 to 18:00.",
    "Books must be returned within 14 days.",
    "Moby Dick by Herman Melville is currently available.",
    "Late returns cost 0.50 euros per day.",
]


fact_vectors = [embed(f) for f in facts]

while True:
    question = input("\nAsk something (or 'quit'): ")
    if question.lower() == "quit":
        break

    q = embed(question)
    scores = [similarity(q, fv) for fv in fact_vectors]

    ranked = sorted(zip(scores, facts), reverse=True)
    for score, fact in ranked[:2]:
        if score <0.400:
            print("I do not have that information")
        else:
            print(f"  {score:.3f}  {fact}")