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
    Description: Generate a number between 3-x.
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


seen_movies_plugin = kernel.import_plugin_from_object(
    MySeenMoviesDatabase(), "SeenMoviesPlugin"
)

load_seen_movies = seen_movies_plugin["LoadSeenMovies"]

sk_prompt = """
You are a wise movie recommender and you have been asked to recommend a movie to a user.
You have a list of movies that the user has watched before.
You want to recommend a movie that the user has not watched before.
Movie List: {{SeenMoviesPlugin.LoadSeenMovies}}.
"""

prompt_template_config = sk.PromptTemplateConfig(
    template=sk_prompt,
    name="tldr",
    template_format="semantic-kernel",
    execution_settings=execution_settings,
)

recommend_function = kernel.create_function_from_prompt(
    prompt_template_config=prompt_template_config,
    function_name="Recommend_Movies",
    plugin_name="Recommendation",
)


async def run_recommendation():
    recommendation = await kernel.invoke(
        recommend_function,
        sk.KernelArguments(),
    )
    print(recommendation)


# Use asyncio.run to execute the async function
asyncio.run(run_recommendation())
