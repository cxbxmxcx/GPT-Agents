import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion

kernel = sk.Kernel()

# Prepare OpenAI service using credentials stored in the `.env` file
api_key, _ = sk.openai_settings_from_dot_env()
kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-4-1106-preview", api_key))

# Alternative using Azure:
# deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
# kernel.add_chat_service("dv", AzureChatCompletion(deployment, endpoint, api_key))

# Wrap your prompt in a function
prompt = kernel.create_semantic_function("""
Please recommend a time travel movie.
""")

# Run your prompt
print(prompt()) 