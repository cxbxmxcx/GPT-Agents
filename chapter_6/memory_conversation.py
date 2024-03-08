from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(input_key="input", output_key="output", llm=llm)
# When added to an agent, the memory object can save pertinent information from conversations or used tools
memory.save_context({"input": "I Like time travel movies"}, {"output": "that's good to know"})
memory.save_context({"input": "I like eating rice"}, {"output": "..."})
memory.save_context({"input": "I don't like driving"}, {"output": "ok"}) 

conversation = ConversationChain(
    llm=llm, verbose=True, memory=memory, output_key="output", input_key="input",
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