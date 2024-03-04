import asyncio

import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.functions import kernel_function

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


class MySeenMoviesDatabase:
    """
    Description: Manages the list of users seen movies.
    """

    @kernel_function(
        description="Loads a list of movies that the user has already seen",
        name="LoadSeenMovies",
    )
    def load_seen_movies(self) -> str:
        try:
            # Open the file in read mode
            with open("seen_movies.txt", "r") as file:
                # Read lines and strip newline characters
                lines = [line.strip() for line in file.readlines()]

                # Join the lines into a comma-separated string
                comma_separated_string = ", ".join(lines)

            return comma_separated_string

        except Exception as e:
            print(f"Error reading file: {e}")
            return None


plugins_directory = "plugins"

recommender = kernel.import_plugin_from_prompt_directory(
    plugins_directory,
    "Recommender",
)

recommend = recommender["Recommend_Movies"]

seen_movies_plugin = kernel.import_plugin_from_object(
    MySeenMoviesDatabase(), "SeenMoviesPlugin"
)

load_seen_movies = seen_movies_plugin["LoadSeenMovies"]


async def show_seen_movies():
    seen_movie_list = await load_seen_movies(kernel)
    return seen_movie_list


seen_movie_list = asyncio.run(show_seen_movies())
print(seen_movie_list)


async def run():
    result = await kernel.invoke(
        recommend,
        sk.KernelArguments(settings=execution_settings, input=seen_movie_list),
    )
    print(result)


asyncio.run(run())
