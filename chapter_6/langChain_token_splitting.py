from dotenv import load_dotenv
import os
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
# Ensure the API key is available
if not api_key:
    raise ValueError("No API key found. Please check your .env file.")

loader = UnstructuredHTMLLoader("sample_documents\mother_goose.html")
data = loader.load()
#print(len(data))

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=50, chunk_overlap=10
)

documents = text_splitter.split_documents(data)
# extract page content from the documents
documents = [doc for doc in documents][8:94]  # capture just the rhymes

db = Chroma.from_documents(documents, OpenAIEmbeddings())


def query_documents(query, top_n=2):
    docs = db.similarity_search(query, top_n)    
    return docs        

# Input Loop for Search Queries
while True:
    query = input("Enter a search query (or 'exit' to stop): ")
    if query.lower() == 'exit':
        break
    top_n = int(input("How many top matches do you want to see? "))
    search_results = query_documents(query, top_n)
    
    print("Top Matched Documents:")
    for i, doc in enumerate(search_results):
        print(f"Document {i+1}: {doc.page_content}")

    print("\n")
