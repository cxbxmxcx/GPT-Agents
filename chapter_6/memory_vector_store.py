from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains import ConversationChain
import faiss
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import FAISS

embedding_size = 1536 # Dimensions of the OpenAIEmbeddings
index = faiss.IndexFlatL2(embedding_size)
embedding_fn = OpenAIEmbeddings()
vectorstore = FAISS(embedding_fn, index, InMemoryDocstore({}), {})

retriever = vectorstore.as_retriever(search_kwargs=dict(k=3))
memory = VectorStoreRetrieverMemory(retriever=retriever, input_key="input", output_key="output")

# When added to an agent, the memory object can save pertinent information from conversations or used tools
memory.save_context({"input": "I Like time travel movie genre"}, {"output": "that's good to know"})
memory.save_context({"input": "I like eating rice"}, {"output": "..."})
memory.save_context({"input": "I don't like driving"}, {"output": "ok"}) #

print(memory.load_memory_variables({"input": "what movie should i watch?"})["history"])

load_dotenv()
llm = ChatOpenAI(temperature=0) # Can be any valid LLM

conversation = ConversationChain(
    llm=ChatOpenAI(temperature=0),    
    memory=memory,
    verbose=True
)

# Input Loop for Search Queries
while True:
    query = input("You (or 'exit' to stop): ")
    if query.lower() == 'exit':
        break
    
    history = memory.load_memory_variables({"input": query})["history"]
    response = conversation.predict(input=query, history=history)    
    memory.save_context({"input": query}, {"output": response})  
    print("Bot: ", response)
    print("\n")