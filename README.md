# Library Support Bot

This is an AI support bot for my library system. You can ask it about the library's rules,
opening hours and books, and it answers using **live data from my own C++ Library Management
System**. If it doesn't have the information, it says so instead of making something up.

```
You:  Is The Hunger Games available?
Bot:  No, "The Hunger Games" by Suzanne Collins is currently borrowed and not available.
You:  Who wrote it?
Bot:  The Hunger Games was written by Suzanne Collins.
```

It works using RAG (retrieval-augmented generation). I didn't train my own AI model. I used
OpenAI's models and built the whole system around them: the search, the safety checks, the
memory, the connection to my library system and the web chat.

---

## How I built it

### 1. Talking to an AI from Python
I started off by writing my first call to the OpenAI API with a system message (how the AI
should act) and a user message (what the person types).

- By changing the **temperature**, I saw that a high temperature made the replies more
  creative and human-like, while a low temperature gave a more robotic feel. For a support
  bot I kept it low, so it gives the same correct answer every time.
- When I changed the system role to *"You are a pirate who works in a library"*, it replied
  *"Ahoy there! Welcome to the grand library of knowledge, me heartie!"*, which showed me how
  much the system message controls the AI's behaviour.
- When I asked *"Is Moby Dick available?"*, the AI answered confidently that Moby-Dick was
  published in 1851 and is free online. It sounded right, but it had nothing to do with **my**
  library. This is the problem the rest of the project solves.

### 2. Giving the chatbot memory
I learned that the AI doesn't actually remember anything. My program keeps the conversation
in a list and sends the whole list again with every message.

- I told it *"My name is Daniel"* and later asked *"What is my name?"*, and it answered correctly.
- I noticed the tokens used grew with every reply, because the whole conversation gets sent
  again each time. To stop the cost growing forever, I only send the last 6 messages.
- When I moved the conversation list inside the loop, the bot forgot my name, because the
  list was being erased every time the loop ran.

### 3. Searching by meaning with embeddings
Next I used embeddings, which turn text into a list of numbers (a vector) where similar
meanings point in similar directions. I wrote a similarity function (cosine similarity) that
gives a higher score the more similar two texts are.

For example:
- *"How late can I come in?"* vs *"The library is open until 18:00."* scored **0.43**
- *"How late can I come in?"* vs *"Moby Dick is available."* scored **0.12**

The first pair share no words, but the search still matched them by meaning. Then I built a
small search engine that compares a question with every fact and keeps the best matches.

### 4. The full RAG bot
I connected the search to the AI. For each question, the bot finds the 3 most relevant facts
and gives them to the AI with instructions to answer **only** from those facts.

When I asked an irrelevant question like *"What is the weather today?"*, the best fact only
scored about 0.12. If the bot passed that to the AI, it could make up an answer
(hallucinate). So I added two safety layers:

- **Layer 1, a similarity threshold:** if even the best fact scores too low, the bot replies
  *"I don't have that information"* without calling the AI at all.
- **Layer 2, the system prompt:** the AI is told to answer only from the facts, and to reply
  with that same sentence if the facts don't answer the question. This catches questions
  like *"Can I reserve a book?"*, which are about the library but not covered by any fact.

### 5. Connecting it to my library system
I added an **"Export for Chatbot"** option to my C++ Library Management System. It writes one
sentence per book (title, author, availability, times borrowed, rating) plus the totals, and
the bot loads that file together with the library rules.

- **Privacy:** I made sure the export never includes member names or IDs. If I asked
  *"Who borrowed this book?"*, the bot can't answer, because it never received that information.
- **"List all books" didn't work at first**, because the bot only sees the top 3 facts and
  there are 10 books. I fixed it by adding a catalogue line to the export. Then
  *"Show me your collection"* still failed, so I reworded the catalogue line to match how
  people actually ask.

### 6. Web chat
I put the bot in a browser chat using Chainlit. Each visitor gets their own conversation
memory, and follow-up questions work: for *"Who wrote it?"*, the bot searches together with
the previous question, so it still knows which book "it" means.

### 7. Testing it
I wrote `eval.py`, which asks the bot 15 test questions and checks the answers automatically.
It covers normal questions, questions it should refuse, privacy and off-topic requests.

| Threshold | Score |
|-----------|-------|
| 0.40      | 14 / 15 |
| **0.20**  | **15 / 15** |

I first thought a threshold around 0.40 would be right, because most library questions
scored above 0.5. But testing showed *"Show me your collection"* only scored 0.26, because
the catalogue line is long and full of titles. Off-topic questions scored around 0.10–0.12,
so I set the threshold to **0.20**, in the gap between them.

The eval checks for key words in each answer, so it can miss answers that are correct but
worded differently. A bigger test set would make it more reliable.

---

## Project files

| File | What it does |
|------|---------|
| `rag_bot.py` | the main logic: loading the facts, embeddings, search, safety layers and answering |
| `app.py` | the web chat (Chainlit), with separate memory for each user |
| `eval.py` | runs the test questions and gives an accuracy score |
| `library_facts.txt` | the library rules |
| `library_status.txt` | live book data exported from my C++ Library Management System |

## How to run it

It needs Python 3.13. I first used Python 3.15, but some of the web libraries didn't
support it yet.

```
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file with your OpenAI key:
```
OPENAI_API_KEY=your-key-here
```

Then:
```
chainlit run app.py      # web chat at http://localhost:8000
python rag_bot.py        # terminal version that also shows the similarity scores
python eval.py           # runs the tests
```

To update the book data, use option 12 ("Export for Chatbot") in the Library Management
System and restart the bot.

## What I would improve next

- Reload the data automatically when the library exports a new file
- Save the embeddings to a file instead of creating them again every time the bot starts
- Let the AI call a function for "list" and "count" questions instead of relying on search
- A bigger set of test questions

## Built with

Python, OpenAI API (GPT-4o-mini and text-embedding-3-small), NumPy, Chainlit, and C++ for
the library system. I used AI tools as a learning aid while building this project, and I
can explain every part of the code.
