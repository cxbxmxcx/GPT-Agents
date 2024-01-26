from promptflow import tool
from typing import List
from scipy.spatial.distance import cosine

@tool
def cosine_similarity(expected_embedding: List[float],
                      predicted_embedding: List[float]) -> float:
    """
    Calculate the cosine similarity between two embeddings.

    :param embedding1: A list of floats representing the first embedding.
    :param embedding2: A list of floats representing the second embedding.
    :return: The cosine similarity score between the two embeddings.
    """
    return 1 - cosine(expected_embedding, predicted_embedding)