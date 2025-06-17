from app.chatbot import ChatBot

# Instantiate chatbot (no OpenAI key needed for local Ollama model)
chatbot = ChatBot()

test_queries = [
    "Who established SHAR?",
    "SHAR का इतिहास बताओ",
    "Give the contact address of SDSC SHAR.",
    "What kind of biodiversity exists at Sriharikota?",
    "When was SHAR established?",
    "श्रीहरिकोटा का मौसम कैसा होता है?"
]

print("\n📍 Running Chatbot Tests...\n")

for query in test_queries:
    print(f"💬 Query: {query}")
    response = chatbot.ask(query)

    # Safe retrieval and print of top context
    try:
        top_context = chatbot._retrieve_context(query, top_k=1)[0]
        print(f"📘 Top Context Snippet: {top_context[0][:150]}...")
    except Exception as e:
        print(f"⚠️ Failed to retrieve context: {e}")

    print(f"🤖 Response: {response}\n{'-'*50}")
