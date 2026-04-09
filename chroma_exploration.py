import os
import chromadb

# creates a folder where the data will be stored
client = chromadb.PersistentClient(path="./chroma_exploration")

# create or get collection if already exists
# using chroma's default embedding model automatically
collection = client.get_or_create_collection(name="test_notes")

# --- Chunking ---
def chunk_text(text, chunk_size=200):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

# Scanning/Adding Data
notes_dir = "./test_notes" # change to whatever folder in actual app is called

# adding chunks to chroma, chroma automatically creates embeddings for these
print("Add documents to Chroma")
for root_folder, sub_folders, files in os.walk(notes_dir):
    for filename in files:
        if filename.endswith(".txt"): # only txt files rn
            full_path = os.path.join(root_folder, filename) # full computer path to open file

            relative_path = os.path.relpath(full_path, notes_dir) # gets relative path to save in metadata for later

            # opens file
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                continue

            # split file into smaller chunks
            file_chunks = chunk_text(content)

            # prep data for chroma
            ids = [f"{relative_path}_chunk_{i}" for i in range(len(file_chunks))]

            # attach relative path as metadata 
            metadatas = [{"source": relative_path} for _ in file_chunks]

            # add to chroma
            collection.upsert(
                documents=file_chunks,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Indexed: {relative_path} ({len(file_chunks)} chunks)")

print("Data added!\n")

# --- Searching Data ---
user_query = "What is a Common Plains song form?"
print(f"Searching for: '{user_query}'")

results = collection.query(
    query_texts=[user_query],
    n_results=2 #bring back the top 2 matches this time
)

# --- Results ---
print("\n--- Search Results ---")
for i in range(len(results['documents'][0])):
    print(f"\nMatch {i+1}:")
    print("Document Text:", results['documents'][0][i])
    print("Distance Score:", results['distances'][0][i])
    print("Source File:", results['metadatas'][0][i]['source'])