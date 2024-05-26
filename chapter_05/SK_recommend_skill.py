import asyncio

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatCompletion,
)

kernel = sk.Kernel()

useAzureOpenAI = False

# Configure AI service used by the kernel
if useAzureOpenAI:
    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
    azure_chat_service = AzureChatCompletion(
        deployment_name="turbo", endpoint=endpoint, api_key=api_key
    )  # set the deployment name to the value of your chat model
    kernel.add_chat_service("chat_completion", azure_chat_service)
else:
    api_key, _ = sk.openai_settings_from_dot_env()
    oai_chat_service = OpenAIChatCompletion(
        ai_model_id="gpt-4-1106-preview", api_key=api_key
    )
    kernel.add_chat_service("chat-gpt", oai_chat_service)

# note: using plugins from the samples folder
plugins_directory = "plugins"

recommender = kernel.import_semantic_plugin_from_directory(
    plugins_directory, "Recommender"
)

recommend = recommender["Recommend"]


async def get_recommendation(
    subject="time travel", format="movie", genre="medieval", custom="must be a comedy"
):
    context = kernel.create_new_context()
    context["subject"] = subject
    context["format"] = format
    context["genre"] = genre
    context["custom"] = custom
    answer = await recommend.invoke(context=context)
    print(answer)


# Use asyncio.run to execute the async function
input = {
    "subject": "time travel",
    "format": "movie",
    "genre": "medieval",
    "custom": "must be a comedy",
}
asyncio.run(get_recommendation(**input))
