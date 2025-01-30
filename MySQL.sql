CREATE DATABASE chatbot_db;

USE chatbot_db;

CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    role ENUM('user', 'system'),
    content TEXT
);
