import faiss
import pickle
import numpy as np
import mysql.connector
import os
import openai
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from datetime import datetime

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",      # Change to your MySQL username
    "password": "root",  # Change to your MySQL password
    "database": "chatbot_db"
}

# File paths
FAISS_INDEX_FILE = "faiss_index.pkl"
CORPUS_FILE = "processed_corpus.txt"

# OpenAI API Key (or use a local LLM model)
OPENAI_API_KEY = "Your Api Key"

app = Flask(__name__)

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

def get_top_k_chunks(query, faiss_index, k=3):
    """Retrieve top-k most relevant text chunks based on the query."""
    query_embedding = model.encode([query], convert_to_numpy=True)
    _, indices = faiss_index.search(query_embedding, k)

    # Load text chunks
    with open(CORPUS_FILE, "r", encoding="utf-8") as file:
        chunks = file.read().split("\n\n")

    retrieved_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]
    return retrieved_chunks

def generate_response(query, context):
    """Generate an answer using OpenAI's GPT-4 (or GPT-3.5)."""
    openai.api_key = OPENAI_API_KEY
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def save_chat_history(user_query, bot_response):
    """Save chat history to MySQL database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = "INSERT INTO chat_history (timestamp, role, content) VALUES (%s, %s, %s)"
        cursor.execute(query, (datetime.now(), "user", user_query))
        cursor.execute(query, (datetime.now(), "system", bot_response))
        
        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Chat history saved successfully.")
    except Exception as e:
        print(f"⚠️ Error saving chat history: {e}")

# Flask API Routes
@app.route("/chat", methods=["POST"])
def chat():
    """Handle user queries, retrieve relevant chunks, and generate responses."""
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400

    retrieved_chunks = get_top_k_chunks(user_query, faiss_index)
    context = " ".join(retrieved_chunks)
    bot_response = generate_response(user_query, context)

    save_chat_history(user_query, bot_response)

    return jsonify({"query": user_query, "response": bot_response, "retrieved_chunks": retrieved_chunks})

@app.route("/history", methods=["GET"])
def get_history():
    """Retrieve chat history from MySQL."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT 20")

        history = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(history)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    faiss_index = load_faiss_index()
    if faiss_index:
        app.run(debug=True, host="0.0.0.0", port=5000)
