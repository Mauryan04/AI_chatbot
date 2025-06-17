import os
import json

DATA_DIR = "data"
GROUP_SIZE = 2  # Number of paragraphs per chunk


def process_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load {filepath}: {e}")
            return

    # Handle if it's a dict (single document)
    if isinstance(data, dict):
        if isinstance(data.get("content"), list) and all(isinstance(p, str) for p in data["content"]):
            paragraphs = data["content"]
            chunks = []
            for i in range(0, len(paragraphs), GROUP_SIZE):
                chunk = "\n\n".join(paragraphs[i:i + GROUP_SIZE])
                chunks.append({
                    "title": data.get("title", ""),
                    "section": data.get("section", ""),
                    "content": chunk
                })
            save_chunks(filepath, chunks)
        else:
            print(f"⚠️ Skipping (unrecognized structure): {filepath}")
    # Handle if it's already a list of strings or proper format
    elif isinstance(data, list) and all(isinstance(d, dict) and "content" in d for d in data):
        print(f"✅ Already formatted: {filepath}")
    else:
        print(f"⚠️ Skipping (unrecognized structure): {filepath}")


def walk_and_process():
    for root, _, files in os.walk(DATA_DIR):
        for filename in files:
            if filename.endswith(".json"):
                fullpath = os.path.join(root, filename)
                process_file(fullpath)


if __name__ == "__main__":
    walk_and_process()
