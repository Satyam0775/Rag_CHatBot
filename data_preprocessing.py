import os
import re
from typing import List

def load_corpus(file_path: str) -> str:
    """Load text from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def clean_text(text: str) -> str:
    """Clean and normalize text by removing special characters and extra spaces."""
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces and new lines
    text = re.sub(r"[^a-zA-Z0-9.,;?!\s]", "", text)  # Keep only basic punctuation
    return text.strip()

def split_into_chunks(text: str, chunk_size: int = 250) -> List[str]:
    """Split text into smaller chunks of ~200-300 words."""
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

if __name__ == "__main__":
    # Load and process the corpus
    corpus_file = "corpus.txt"  
    text = load_corpus(corpus_file)  
    cleaned_text = clean_text(text)  
    chunks = split_into_chunks(cleaned_text)  

    # Save processed chunks to a new file
    output_file = "processed_corpus.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(chunks))  # Separate chunks by new lines

    print(f"✅ Processed corpus saved in '{output_file}' with {len(chunks)} chunks.")
