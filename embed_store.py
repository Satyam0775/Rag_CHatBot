import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# File paths
CORPUS_FILE = "processed_corpus.txt"
FAISS_INDEX_FILE = "faiss_index.pkl"

def load_chunks(file_path: str):
    """Load processed text chunks from file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().split("\n\n")  # Split chunks by newlines

def generate_embeddings(chunks):
    """Generate embeddings for each text chunk."""
    return model.encode(chunks, convert_to_numpy=True)

def save_faiss_index(embeddings, output_file=FAISS_INDEX_FILE):
    """Save embeddings to FAISS vector database and pickle the index."""
    d = embeddings.shape[1]  # Get embedding dimension
    index = faiss.IndexFlatL2(d)  # L2 distance-based FAISS index
    index.add(embeddings)  # Add embeddings

    # Save index using pickle
    with open(output_file, "wb") as f:
        pickle.dump(index, f)
    print(f"✅ FAISS index saved as '{output_file}'")

def load_faiss_index(file_path=FAISS_INDEX_FILE):
    """Load FAISS index from a pickle file."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            index = pickle.load(f)
        print(f"✅ FAISS index loaded with {index.ntotal} vectors.")
        return index
    else:
        print(f"⚠️ FAISS index file not found! Ensure '{file_path}' exists.")
        return None

if __name__ == "__main__":
    if not os.path.exists(CORPUS_FILE):
        print(f"⚠️ File '{CORPUS_FILE}' not found! Run `data_preprocessing.py` first.")
    else:
        chunks = load_chunks(CORPUS_FILE)  # Load text chunks
        embeddings = generate_embeddings(chunks)  # Create embeddings
        save_faiss_index(embeddings)  # Store embeddings in FAISS

    # Try loading the FAISS index
    load_faiss_index()
