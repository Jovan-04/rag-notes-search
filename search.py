import chromadb
import os
import json

# initialize 
with open(".env") as envfile:
    ENV = {k:v for (k, v) in map(lambda l: l.split('='), envfile.read().splitlines())}

CHROMA_PATH = ENV["CHROMA_PATH"]

# creates a folder where the data will be stored
client = chromadb.PersistentClient(path=CHROMA_PATH)
# create or get collection if already exists
# using chroma's default embedding model automatically
collection = client.get_or_create_collection(name="test_notes")

# tracks which notes have already been processed
time_tracker = os.path.join(CHROMA_PATH, "index_tracker.json")

def build_index():
    def chunk_text(text, chunk_size=200):
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i + chunk_size])
        return chunks

    # checks which files have been indexed
    if os.path.exists(time_tracker):
        with open(time_tracker, 'r') as f:
            indexed_files = json.load(f)
    else:
        indexed_files = {}

    notes_dir = "./Notes" # change to whatever folder notes are in
    made_changes = False

    print("Adding documents to Chroma...")
    for root_folder, sub_folders, files in os.walk(notes_dir):
        for filename in files:
            if filename.endswith((".txt", ".md")):
                full_path = os.path.join(root_folder, filename)
                relative_path = os.path.relpath(full_path, notes_dir)

                # getting time of when file was last modified by computer
                current_mtime = os.path.getmtime(full_path)
                # checks if the exact file and timestamps match, meaning nothing has changed and file can be skipped
                if relative_path in indexed_files and indexed_files[relative_path] == current_mtime:
                    continue

                print(f"Processing updated/new file: {relative_path}")

                # will only process new or edited files
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if not content.strip():
                    continue

                file_chunks = chunk_text(content)
                ids = [f"{relative_path}_chunk_{i}" for i in range(len(file_chunks))]
                metadatas = [{"source": relative_path} for _ in file_chunks]

                collection.upsert(documents=file_chunks, metadatas=metadatas, ids=ids)
                indexed_files[relative_path] = current_mtime
                made_changes = True
            
    if made_changes:
        with open(time_tracker, 'w') as f:
            json.dump(indexed_files, f)
        print("Finished updating the index!\n")
    else:
        print("No changes detected. Index is already up to date!\n")

def search(user_query: str):
    print(f"Searching for: '{user_query}'")

    results = collection.query(
        query_texts=[user_query],
        n_results=2 
    )

    # formatting results into python list of dictionaries to be sent over the web
    formatted_results = []
    
    if results['documents'] and results['documents'][0]:
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                "match_number": i + 1,
                "document_text": results['documents'][0][i],
                "distance_score": results['distances'][0][i],
                "source_file": results['metadatas'][0][i]['source']
            })
            
    return formatted_results


# for testing purposes
if __name__ == "__main__":

    build_index()

    # testing the search function
    print("\n--- TESTING SEARCH ---")
    test_answer = search("what is the dsm5?")

    # Print the resulting dictionary cleanly
    import pprint
    pprint.pprint(test_answer)