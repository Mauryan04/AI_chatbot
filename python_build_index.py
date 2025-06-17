import faiss
import os
import json
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Paths
data_folder = "data"
index_path = "embeddings/faiss_index.index"
embedding_model = "all-MiniLM-L6-v2"

# Load model
model = SentenceTransformer(embedding_model)

# Load documents from JSON files
documents = []
metadata = []

print("📂 Scanning files...")
for root, _, files in os.walk(data_folder):
    for filename in files:
        if filename.endswith(".json"):
            path = os.path.join(root, filename)
            with open(path, encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    print(f"📄 Loaded {filename} with {len(data)} records")
                    for entry in data:
                        if isinstance(entry, dict):
                            text_parts = []
                            # Combine all relevant fields
                            for key in ["title", "content", "description"]:
                                if key in entry:
                                    text_parts.append(str(entry[key]))
                            full_text = "\n".join(text_parts).strip()
                            if full_text:
                                documents.append(full_text)
                                metadata.append({
                                    "file": filename,
                                    "title": entry.get("title", "N/A"),
                                    "section": entry.get("section", "N/A")
                                })
                        else:
                            print(f"⚠️ Skipping non-dict entry in {filename}")
                except Exception as e:
                    print(f"❌ Failed to parse {filename}: {e}")

print(f"📊 Total documents prepared: {len(documents)}")

# Generate embeddings
print("🔍 Generating sentence embeddings...")
embeddings = model.encode(documents, show_progress_bar=True)

# Create FAISS index
dim = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings))
faiss.write_index(index, index_path)

print(f"✅ Saved FAISS index to {index_path} with {len(documents)} vectors")


# ✅ Save metadata alongside the index
with open("embeddings/metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("📝 Metadata saved to embeddings/metadata.json")