import faiss
import numpy as np
import json
import os
import re
import requests
from sentence_transformers import SentenceTransformer
import langdetect  # NEW: basic language detection

# 🔁 Keyword reranker using keyword overlap
def keyword_rerank(query: str, docs, top_n=3):
    keywords = re.findall(r'\w+', query.lower())
    ranked = []
    for doc in docs:
        text = doc["page_content"].lower()
        score = sum(1 for word in keywords if word in text)
        ranked.append((score, doc))
    ranked.sort(reverse=True, key=lambda x: x[0])
    return [doc for _, doc in ranked[:top_n]]

class ChatBot:
    def __init__(self,
                 index_path="embeddings/faiss_index.index",
                 data_folder="data",
                 embedding_model="all-MiniLM-L6-v2",
                 verbose=True):

        self.verbose = verbose
        self.index = faiss.read_index(index_path)
        self.documents = self._load_documents(data_folder)
        self.embedder = SentenceTransformer(embedding_model)
        if self.verbose:
            print(f"✅ Embedding model loaded: {embedding_model}")

    def _load_documents(self, data_folder):
        docs = []
        for root, _, files in os.walk(data_folder):
            for filename in files:
                if filename.endswith(".json"):
                    fullpath = os.path.join(root, filename)
                    with open(fullpath, encoding="utf-8") as f:
                        try:
                            data = json.load(f)
                            for entry in data:
                                content = entry.get("content", "")
                                if isinstance(content, list):
                                    content = "\n".join(content)
                                metadata = {
                                    "title": entry.get("title", ""),
                                    "section": entry.get("section", ""),
                                    "source": filename
                                }
                                docs.append((content, metadata))
                        except Exception as e:
                            print(f"❌ Failed to load {filename}: {e}")
        return docs

    def _retrieve_context(self, query, top_k=8):
        query_vec = self.embedder.encode([query])
        D, I = self.index.search(np.array(query_vec), top_k * 2)  # Over-fetch
        results = [(self.documents[i][0], self.documents[i][1]) for i in I[0]]

        # Metadata-boosted reranking
        keywords = set(re.findall(r'\w+', query.lower()))
        def boost_score(doc):
            meta = doc[1]
            meta_text = f"{meta.get('title', '')} {meta.get('section', '')}".lower()
            return sum(1 for word in keywords if word in meta_text)

        results.sort(key=boost_score, reverse=True)
        return results[:top_k]

    def _generate_answer(self, prompt: str) -> str:
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "mistral", "prompt": prompt, "stream": False}
            )
            return response.json()["response"]
        except Exception as e:
            return f"❌ Failed to generate answer: {e}"

    def ask(self, query: str) -> str:
        # 🌐 Detect language
        lang = langdetect.detect(query)
        is_hindi = lang == 'hi'

        # 📚 Retrieve relevant documents
        raw_docs = self._retrieve_context(query, top_k=8)
        valid_docs = [{"page_content": t, "meta": m} for t, m in raw_docs if len(t.strip()) > 30]
        if not valid_docs:
            return "Sorry, I don’t have that information."

        # 🧠 Keyword rerank
        top_docs = keyword_rerank(query, valid_docs, top_n=3)
        if not top_docs:
            top_docs = valid_docs[:3]

        # 🧾 Context formatting
        context = "\n\n".join(
            f"[Title: {doc['meta']['title']} | Section: {doc['meta']['section']} | Source: {doc['meta']['source']}]\n{doc['page_content']}"
            for doc in top_docs
        )

        prompt_intro = (
            "You are a knowledgeable assistant for SDSC SHAR (ISRO's launch site). "
            "Answer clearly using only the context. If unsure, say 'Sorry, I don't know.'\n\n"
        )

        if is_hindi:
            prompt_intro = (
                "आप SDSC SHAR (ISRO के प्रक्षेपण स्थल) के लिए एक जानकार सहायक हैं। "
                "केवल दिए गए संदर्भ का उपयोग करके स्पष्ट उत्तर दें। अगर जानकारी न हो तो कहें 'माफ़ कीजिए, मुझे नहीं पता।'\n\n"
            )

        prompt = f"{prompt_intro}Context:\n{context}\n\nQuestion: {query}\nAnswer:"

        answer = self._generate_answer(prompt)

        # 📉 Heuristic: short or vague response
        if len(answer.strip()) < 20 or "don't know" in answer.lower():
            return "Sorry, I couldn’t find a confident answer for that."

        return answer
