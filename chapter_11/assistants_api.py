import openai
from dotenv import load_dotenv

load_dotenv()

# OpenAI client initialization
client = openai.OpenAI()

class AssistantsAPI():
    # def create_assistant(self, name, instructions, model, tools):
    #     assistant = client.beta.assistants.create(
    #         name=name,
    #         instructions=instructions,
    #         tools=tools,
    #         model=model
    #     )
    #     return assistant
    
    def create_assistant(self, name, instructions, model, tools, files, response_format, temperature, top_p):
        return None

    def list_assistants(self):
        assistants = client.beta.assistants.list(limit=100)
        return assistants

    def retrieve_assistant(self, assistant_id):
        try:
            assistant = client.beta.assistants.retrieve(assistant_id)        
            return assistant
        except Exception:
            return None

    # def update_assistant(self, assistant_id, name, instructions, model, tools):
    #     assistant = client.beta.assistants.update(
    #         assistant_id,
    #         name=name,
    #         instructions=instructions,
    #         model=model,
    #         tools=tools
    #     )
    #     return assistant
    
    def update_assistant(self,  assistant_name, assistant_id, assistant_instructions, assistant_model, assistant_tools, assistant_files, assistant_resformat, assistant_temperature, assistant_top_p):
        # assistant = client.beta.assistants.update(
        #     assistant_id,
        #     name=assistant_name,
        #     instructions=assistant_instructions,
        #     model=assistant_model,
        #     tools=assistant_tools,            
        #     response_format=assistant_resformat,
        #     temperature=assistant_temperature,
        #     top_p=assistant_top_p
        # )
        # return assistant
        return 

    def delete_assistant(self, assistant_id):
        client.beta.assistants.delete(assistant_id)
        
api = AssistantsAPI()

# asss = api.list_assistants()
# for a in asss.data:
#     if a.name == "Sample Assistant":
#         api.delete_assistant(a.id)
        