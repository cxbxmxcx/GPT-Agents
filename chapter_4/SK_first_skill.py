import asyncio

import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai

selected_service = "OpenAI"
kernel = sk.Kernel()

service_id = None
if selected_service == "OpenAI":
    from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

    api_key, org_id = sk.openai_settings_from_dot_env()
    service_id = "oai_chat_gpt"
    model_id = "gpt-4-1106-preview"
    kernel.add_service(
        OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=model_id,
            api_key=api_key,
            org_id=org_id,
        ),
    )
elif selected_service == "AzureOpenAI":
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
    service_id = "aoai_chat_completion"
    kernel.add_service(
        AzureChatCompletion(
            service_id=service_id,
            deployment_name=deployment,
            endpoint=endpoint,
            api_key=api_key,
        ),
    )

# set up the execution settings
if selected_service == "OpenAI":
    execution_settings = sk_oai.OpenAIChatPromptExecutionSettings(
        service_id=service_id,
        ai_model_id=model_id,
        max_tokens=2000,
        temperature=0.7,
    )
elif selected_service == "AzureOpenAI":
    execution_settings = sk_oai.OpenAIChatPromptExecutionSettings(
        service_id=service_id,
        ai_model_id=deployment,
        max_tokens=2000,
        temperature=0.7,
    )
# note: using plugins from the samples folder
plugins_directory = "plugins"

recommender = kernel.import_plugin_from_prompt_directory(
    plugins_directory,
    "Recommender",
)

recommend = recommender["Recommend_Movies"]

seen_movie_list = [
    "Back to the Future",
    "The Terminator",
    "12 Monkeys",
    "Looper",
    "Groundhog Day",
    "Primer",
    "Donnie Darko",
    "Interstellar",
    "Time Bandits",
    "Doctor Strange",
]


async def run():
    result = await kernel.invoke(
        recommend,
        sk.KernelArguments(
            settings=execution_settings, input=", ".join(seen_movie_list)
        ),
    )
    print(result)


asyncio.run(run())
