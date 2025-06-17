Here’s a clean and informative `README.md` for your **SDSC SHAR Chatbot** project, ready to upload to GitHub:

---

### ✅ `README.md`

```markdown
# SDSC SHAR Chatbot 🚀

This is a multilingual AI-powered chatbot designed to answer questions about [ISRO's](https://www.isro.gov.in) **Satish Dhawan Space Centre SHAR (SDSC SHAR)**. It uses local embeddings, semantic search with FAISS, and the open-source `mistral` model via [Ollama](https://ollama.com) for inference.

---

## 💡 Features

- 🔎 Contextual semantic search using sentence embeddings (MiniLM)
- 🧠 Local large language model (Mistral via Ollama)
- 🌐 Multilingual support (English, Hindi, Hinglish, etc.)
- ⚡ Fast local inference without OpenAI API
- 🧩 Modular codebase and lightweight UI

---

## 📁 Folder Structure

```

shar-chatbot/
│
├── app/
│   └── chatbot.py         # Core logic for embeddings, retrieval, and generation
│
├── data/                  # JSON files with SHAR information
│
├── embeddings/
│   ├── faiss\_index.index  # FAISS vector index
│   └── metadata.json      # Metadata for retrieved documents
│
├── static/
│   ├── index.html         # Frontend UI
│   ├── style.css          # Chat styling
│   └── script.js          # Chat behavior and API integration
│
├── api.py                 # Flask API for backend
├── test\_chat.py           # Local console test script
├── .gitignore
├── requirements.txt
└── README.md

````

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/shar-chatbot.git
cd shar-chatbot
````

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# Or
source venv/bin/activate  # On Linux/macOS
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Build embeddings

```bash
python build_index.py
```

---

## 🧠 Run Ollama (Mistral Model)

Install [Ollama](https://ollama.com) and run:

```bash
ollama pull mistral
ollama run mistral
```

> Ollama must be running locally for the chatbot to generate responses.

---

## 🖥️ Start the Flask API

```bash
python api.py
```

---

## 🌐 Open the Frontend

Open `index.html` in your browser (double-click or serve via VSCode Live Server).

---

## 🌍 Expose for External Use (Optional)

To share your chatbot on other devices or with friends:

```bash
ngrok config add-authtoken YOUR_TOKEN
ngrok http 5000
```

Then open the forwarded link (e.g., `https://xxxxx.ngrok-free.app`) in the browser.

---

## 🤝 Contributing

Pull requests and suggestions are welcome. For major changes, please open an issue first.

---

## 📜 License

MIT License. You are free to use, modify, and distribute this chatbot.

---

## ✨ Author

Built with ❤️ by **Ishan Bajpai** – Master's Student at IIT Ropar & IIM Amritsar

```

---

Let me know if you'd like to add badges, GitHub Pages hosting instructions, or a contributors section.
```
