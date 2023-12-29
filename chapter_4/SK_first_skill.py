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
    
# note: using skills from the samples folder
skills_directory = "skills"

recommender = kernel.import_semantic_skill_from_directory(skills_directory, "Recommender")

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
    "Doctor Strange"
]

result = recommend("".join(seen_movie_list))

print(result)