from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

load_dotenv()

memory = ConversationBufferMemory(input_key="input",
                                  output_key="output",
                                  llm=ChatOpenAI(temperature=0))

# When added to an agent, the memory object can save pertinent information from conversations or used tools
memory.save_context({"input": "I Like time travel movies"},
                    {"output": "that's good to know"})
memory.save_context({"input": "I like eating rice"},
                    {"output": "..."})
memory.save_context({"input": "I don't like driving"},
                    {"output": "ok"}) #

print(memory.load_memory_variables({"input": "what movie should i watch?"})["history"])



