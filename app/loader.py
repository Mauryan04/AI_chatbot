import os
import json
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class DocumentLoader:
    def __init__(self, data_folder="data", embedding_model_name="all-MiniLM-L6-v2"):
        self.data_folder = data_folder
        self.model = SentenceTransformer(embedding_model_name)
        self.index = None
        self.documents = []  # List of (text, metadata)

    def load_json_files(self):
        for filename in os.listdir(self.data_folder):
            if filename.endswith(".json"):
                filepath = os.path.join(self.data_folder, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for entry in data:
                        content = entry.get("content", "")
                        metadata = {
                            "title": entry.get("title", ""),
                            "section": entry.get("section", ""),
                            "source": filename
                        }
                        self.documents.append((content, metadata))

    def build_faiss_index(self):
        texts = [doc[0] for doc in self.documents]
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        return self.index

    def save_index(self, path="embeddings/faiss_index.index"):
        if self.index is not None:
            faiss.write_index(self.index, path)

    def get_documents(self) -> List[Tuple[str, dict]]:
        return self.documents
