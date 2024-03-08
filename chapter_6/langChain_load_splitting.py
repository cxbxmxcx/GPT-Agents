from openai import OpenAI
from dotenv import load_dotenv
import os
import chromadb
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
# Ensure the API key is available
if not api_key:
    raise ValueError("No API key found. Please check your .env file.")
client = OpenAI(api_key=api_key)


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding


loader = UnstructuredHTMLLoader("sample_documents\mother_goose.html")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=25,
    length_function=len,
    add_start_index=True,
)
documents = text_splitter.split_documents(data)
# extract page content from the documents
documents = [doc.page_content for doc in documents][100:350]  # only use 250 documents/chunks (cheaper and faster)

# Generate embeddings for each document
embeddings = [get_embedding(doc) for doc in documents]
ids = [f"id{i}" for i in range(len(documents))]

#create chroma database client
chroma_client = chromadb.Client()
#create a collection
collection = chroma_client.create_collection(name="documents")

collection.add(
    embeddings=embeddings,
    documents=documents,    
    ids=ids
)

def query_chromadb(query, top_n=2):
    """Returns the text of the top 2 results from the ChromaDB collection
    """    
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],    
        n_results=top_n
    )
    return [(id, score, text) for id, score, text in 
            zip(results['ids'][0], results['distances'][0], results['documents'][0])]
        

# Input Loop for Search Queries
while True:
    query = input("Enter a search query (or 'exit' to stop): ")
    if query.lower() == 'exit':
        break
    top_n = int(input("How many top matches do you want to see? "))
    search_results = query_chromadb(query, top_n)
    
    print("Top Matched Documents:")
    for id, score, text in search_results:
        print(f"ID:{id} TEXT: {text} SCORE: {round(score, 2)}")

    print("\n")
