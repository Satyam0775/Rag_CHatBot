# Save the provided text content as corpus.txt
content = """Machine learning (ML) is a field of artificial intelligence (AI) that focuses on using data and algorithms to imitate the way humans learn, gradually improving its accuracy. Machine learning allows software applications to become more accurate in predicting outcomes without being explicitly programmed to do so.

The process of machine learning begins with feeding training data to an algorithm. Training data is a set of data that includes both input and the corresponding correct output. This enables the algorithm to find patterns and correlations.

There are three main types of machine learning:
1. Supervised learning: Involves labeled data and aims to predict outcomes.
2. Unsupervised learning: Involves unlabeled data and aims to find hidden patterns.
3. Reinforcement learning: Focuses on learning through interaction with an environment to maximize cumulative rewards.

Applications of machine learning are vast and include image recognition, natural language processing, and predictive analytics. It is widely used in healthcare, finance, and autonomous driving systems."""

# Save content to corpus.txt
with open("corpus.txt", "w", encoding="utf-8") as file:
    file.write(content)

print("corpus.txt has been created successfully.")
