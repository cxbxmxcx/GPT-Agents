import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
import asyncio

kernel = sk.Kernel()

# Prepare OpenAI service using credentials stored in the `.env` file
api_key, _ = sk.openai_settings_from_dot_env()
kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-4-1106-preview", api_key))

# Alternative using Azure:
# deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
# kernel.add_chat_service("dv", AzureChatCompletion(deployment, endpoint, api_key))

# Wrap your prompt in a function
recommend = kernel.create_semantic_function("""
system:

You have vast knowledge of everything and can recommend anything provided you are given the following criteria, the subject, genre, format and any other custom information.

user:
Please recommend a {{$format}} with the subject {{$subject}} and {{$genre}}. 
Include the following custom information: {{$custom}}
""")

# Define get_recommendation as an async function
async def get_recommendation(subject="time travel",
                             format="movie",
                             genre="medieval",
                             custom="must be a comedy"):
    context = kernel.create_new_context()
    context["subject"] = subject
    context["format"] = format
    context["genre"] = genre
    context["custom"] = custom
    answer = await recommend.invoke_async(context=context)
    print(answer)

# Use asyncio.run to execute the async function
asyncio.run(get_recommendation())

