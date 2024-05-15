from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler

client = OpenAI()

assistant = client.beta.assistants.create(
  name="Sample Assistant",
  instructions="You are an assistant that provides coding advice. Answer coding queries and run code snippets when necessary.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo"
)
            
            
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I'm struggling with Python lists. Can you show me how to append an item?"
)

run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages)
else:
  print(run.status)

