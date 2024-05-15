from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv
from typing_extensions import override
from openai import AssistantEventHandler


load_dotenv()
client = OpenAI()

assistant = client.beta.assistants.create(
  name="Sample Assistant",
  instructions="You are an assistant that provides coding advice. Answer coding queries and run code snippets when necessary.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo" 
)           
            
thread = client.beta.threads.create()  # create a new thread everytime this is run

def ask_assistant(message, history):
    # history is not used here because the thread manages history
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )
    partial_msg = ""
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,      
    ) as stream:        
        for text in stream.text_deltas:
            partial_msg += text
            yield partial_msg

gr.ChatInterface(ask_assistant).launch()