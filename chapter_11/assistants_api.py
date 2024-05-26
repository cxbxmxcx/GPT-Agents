import openai
from dotenv import load_dotenv

load_dotenv()


class AssistantsAPI:
    def __init__(self):
        self.client = openai.OpenAI()

    def create_thread(self):
        return self.client.beta.threads.create()

    def create_thread_message(self, thread_id, role, content):
        return self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=content,
        )

    def create_assistant(
        self,
        name,
        instructions,
        model,
        tools,
        files,
        response_format,
        temperature,
        top_p,
    ):
        assistant = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model,
            tools=tools,
            response_format=response_format,
            temperature=temperature,
            top_p=top_p,
        )
        return assistant

    def run_stream(self, thread_id, assistant_id, event_handler):
        return self.client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=event_handler,
        )

    def list_assistants(self):
        assistants = self.client.beta.assistants.list(limit=100)
        return assistants

    def retrieve_assistant(self, assistant_id):
        try:
            assistant = self.client.beta.assistants.retrieve(assistant_id)
            return assistant
        except Exception:
            return None

    def update_assistant(
        self,
        assistant_name,
        assistant_id,
        assistant_instructions,
        assistant_model,
        assistant_tools,
        assistant_files,
        assistant_resformat,
        assistant_temperature,
        assistant_top_p,
    ):
        assistant = self.client.beta.assistants.update(
            assistant_id,
            name=assistant_name,
            instructions=assistant_instructions,
            model=assistant_model,
            tools=assistant_tools,
            response_format=assistant_resformat,
            temperature=assistant_temperature,
            top_p=assistant_top_p,
        )
        return assistant

    def delete_assistant(self, assistant_id):
        self.client.beta.assistants.delete(assistant_id)


api = AssistantsAPI()

# asss = api.list_assistants()
# for a in asss.data:
#     if a.name == "Sample Assistant":
#         api.delete_assistant(a.id)
