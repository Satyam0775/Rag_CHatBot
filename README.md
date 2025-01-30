# RAG Chatbot Project

## Overview
This project implements a **Retrieval-Augmented Generation (RAG)** chatbot using a vector database and a Flask API. The chatbot retrieves relevant information from a small text corpus based on user queries and generates answers using a generative model. The system stores chat history in a MySQL database for future reference.

## Folder Structure

## Prerequisites
Make sure you have the following installed:
- Python 3.x
- MySQL (for storing chat history)
- Virtual environment tools like `venv` or `conda` (optional but recommended)

## Setup Instructions

### 1. Clone the repository
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/rag-chatbot.git
python -m venv rag-chatbot-env
source rag-chatbot-env/bin/activate   # On Windows: rag-chatbot-env\Scripts\activate
mysql -u root -p
CREATE DATABASE rag_chatbot_db;
