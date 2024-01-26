from promptflow import tool
from typing import List
import numpy as np
from scipy.spatial.distance import cosine

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def consistency(texts: List[str], 
                embeddings: List[List[float]]) -> str:
    if len(embeddings) != len(texts):
        raise ValueError("The number of embeddings must match the number of texts.")

    # Calculate the mean of all embeddings
    mean_embedding = np.mean(embeddings, axis=0)

    # Calculate cosine similarity of each embedding with the mean embedding
    similarities = [1 - cosine(embedding, mean_embedding) for embedding in embeddings]

    # Find the index of the embedding with the highest similarity
    most_similar_index = np.argmax(similarities) 
    
    # Log metric
    from promptflow import log_metric
    log_metric(key="highest_ranked_output", value=texts[most_similar_index])

    return texts[most_similar_index]
