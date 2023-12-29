import asyncio
from semantic_kernel.skill_definition import sk_function
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion

kernel = sk.Kernel()

useAzureOpenAI = False

# Configure AI service used by the kernel
if useAzureOpenAI:
    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
    azure_chat_service = AzureChatCompletion(deployment_name="turbo", endpoint=endpoint, api_key=api_key)   # set the deployment name to the value of your chat model
    kernel.add_chat_service("chat_completion", azure_chat_service)
else:
    api_key, _ = sk.openai_settings_from_dot_env()
    oai_chat_service = OpenAIChatCompletion(ai_model_id="gpt-4-1106-preview", api_key=api_key)
    kernel.add_chat_service("chat-gpt", oai_chat_service)


class MySeenMoviesDatabase:
    """
    Description: Manages the list of users seen movies.
    """
    @sk_function(
        description="Loads a list of movies that the user has already seen",
        name="LoadSeenMovies",
    )
    def load_seen_movies(self) -> str:        
        try:
            # Open the file in read mode
            with open("seen_movies.txt", 'r') as file:
                # Read lines and strip newline characters
                lines = [line.strip() for line in file.readlines()]

                # Join the lines into a comma-separated string
                comma_separated_string = ', '.join(lines)

            return comma_separated_string

        except Exception as e:
            print(f"Error reading file: {e}")
            return None
        
        
skills_directory = "skills"

recommender = kernel.import_semantic_skill_from_directory(skills_directory, "Recommender")

recommend = recommender["Recommend_Movies"]

seen_movies_skill = kernel.import_skill(MySeenMoviesDatabase())

load_seen_movies = seen_movies_skill["LoadSeenMovies"]
seen_movie_list = load_seen_movies()
print(seen_movie_list)

async def main():
    result = await recommend.invoke_async(str(seen_movie_list))
    print(result)

# Run the event loop
asyncio.run(main())



