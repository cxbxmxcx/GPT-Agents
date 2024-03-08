import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample Documents
documents = [
    "The sky is blue and beautiful.",
    "Love this blue and beautiful sky!",
    "The quick brown fox jumps over the lazy dog.",
    "A king's breakfast has sausages, ham, bacon, eggs, toast, and beans",
    "I love green eggs, ham, sausages and bacon!",
    "The brown fox is quick and the blue dog is lazy!",
    "The sky is very blue and the sky is very beautiful today",
    "The dog is lazy but the brown fox is quick!"
]

# Vectorization using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

# Calculating Cosine Similarity
cosine_similarities = cosine_similarity(X)

while True:
    # User input for selecting a document
    selected_document_index = input(f"Enter a document number (0-{len(documents)-1}) or 'exit' to quit: ").strip()
    
    if selected_document_index.lower() == 'exit':
        break

    if not selected_document_index.isdigit() or not 0 <= int(selected_document_index) < len(documents):
        print("Invalid input. Please enter a valid document number.")
        continue

    selected_document_index = int(selected_document_index)

    # Extracting similarity scores for the selected document
    selected_document_similarities = cosine_similarities[selected_document_index]

    # Truncate long document texts for x-axis labels
    x_axis_labels = [doc[:50] + "..." if len(doc) > 50 else doc for doc in documents]

    # Plotting the cosine similarity
    fig = go.Figure([go.Bar(x=x_axis_labels, 
                            y=selected_document_similarities)])

    fig.update_layout(title=f"Cosine Similarities of '{documents[selected_document_index][:50] + '...' if len(documents[selected_document_index]) > 50 else documents[selected_document_index]}' with Others",
                      xaxis_title="Document",
                      yaxis_title="Cosine Similarity",
                      xaxis={'tickangle': 45})  # Rotate x-axis labels for better readability

    fig.show()
