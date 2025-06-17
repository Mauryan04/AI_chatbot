from app.loader import DocumentLoader

loader = DocumentLoader(data_folder="data")
loader.load_json_files()
loader.build_faiss_index()
loader.save_index()

print("Loaded documents:")
for doc in loader.get_documents():
    print(doc[1]['title'], "→", doc[0][:60], "...")
