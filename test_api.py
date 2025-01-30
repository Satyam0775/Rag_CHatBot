import requests

def test_chat():
    response = requests.post("http://127.0.0.1:5000/chat", json={"query": "What is RAG?"})
    assert response.status_code == 200

def test_history():
    response = requests.get("http://127.0.0.1:5000/history")
    assert response.status_code == 200
