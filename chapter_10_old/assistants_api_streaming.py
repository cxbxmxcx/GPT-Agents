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


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print("assistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"assistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
        if delta.code_interpreter.outputs:
            print("\noutput >", flush=True)
            for output in delta.code_interpreter.outputs:
                if output.type == "logs":
                    print(f"{output.logs}", flush=True)
            
            
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I'm struggling with Python lists. Can you show me how to append an item?"
)

# Using the EventHandler to stream the response
with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  event_handler=EventHandler(),
) as stream:
  stream.until_done()

