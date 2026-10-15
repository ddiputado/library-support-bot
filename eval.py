from rag_bot import answer

REFUSAL = "I don't have that information"

tests = [
    ("How many books can I borrow at once?", ["3"]),
    ("Is The Hunger Games available?",       ["not available"]),
    ("Who wrote The Hobbit?",                ["Tolkien"]),
    ("When does the library close?",         ["18:00"]),
    ("How much is the late fee?",            ["0.50"]),
    ("How long can I keep a book?",          ["14"]),
    ("How many books does the library have?", ["10"]),
    ("Is membership free?",                  ["free"]),
    ("What's the weather today?",            None),
    ("Who borrowed Frankenstein?",           None),
    ("Can I reserve a book?",                None),
    ("Write me a poem about pizza",          None),
    ("Show me your collection",              ["Hobbit"]),
    ("I want something by Mary Shelley",     ["Frankenstein"]),
    ("Can I take out four books together?",  ["3"]),
    
]

passed = 0
for question, expected in tests:
    reply, used = answer(question)

    if expected is None:
        ok = REFUSAL.lower() in reply.lower()
    else:
        ok = all(word.lower() in reply.lower() for word in expected)

    if ok:
        passed +=1
    print(f"{'Pass' if ok else 'FAIL'} | {question}")
    print(f"       -> {reply}\n")

print(f"Score: {passed}/{len(tests)} ({passed/ len(tests):.0%})")