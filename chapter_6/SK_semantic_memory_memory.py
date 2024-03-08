import asyncio
from typing import Tuple
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAITextEmbedding,
    AzureChatCompletion,
    AzureTextEmbedding
)

kernel = sk.Kernel()

useAzureOpenAI = False

# Configure AI service used by the kernel
if useAzureOpenAI:
    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
    # next line assumes chat deployment name is "turbo", adjust the deployment name to the value of your chat model if needed
    azure_chat_service = AzureChatCompletion(deployment_name="turbo", endpoint=endpoint, api_key=api_key)
    # next line assumes embeddings deployment name is "text-embedding", adjust the deployment name to the value of your chat model if needed  
    azure_text_embedding = AzureTextEmbedding(deployment_name="text-embedding", endpoint=endpoint, api_key=api_key)
    kernel.add_chat_service("chat_completion", azure_chat_service)
    kernel.add_text_embedding_generation_service("ada", azure_text_embedding)
else:
    api_key, _ = sk.openai_settings_from_dot_env()
    oai_chat_service = OpenAIChatCompletion(ai_model_id="gpt-4-1106-preview", api_key=api_key)
    oai_text_embedding = OpenAITextEmbedding(ai_model_id="text-embedding-ada-002", api_key=api_key)
    kernel.add_chat_service("chat-gpt", oai_chat_service)
    kernel.add_text_embedding_generation_service("ada", oai_text_embedding)

kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())
kernel.import_skill(sk.core_skills.TextMemorySkill())

async def populate_memory(kernel: sk.Kernel) -> None:
    # Add some documents to the semantic memory
    await kernel.memory.save_information_async(
        collection="preferences",
        id="info1", 
        text="My subject preference is time travel "
    )
    await kernel.memory.save_information_async(
        collection="preferences", 
        id="info2", 
        text="My genre preference is science fiction"
    )
    await kernel.memory.save_information_async(
       collection= "preferences",
       id="info3", 
       text="my format preference is TV shows"
    )
    await kernel.memory.save_information_async(
        collection="preferences",
        id="info4",
        text="I dislike old movies (before 1960)"
    )
    await kernel.memory.save_information_async(
        collection="preferences",
        id="info5",
        text="My favorite actor is Chris Pine"
    )    

async def search_memory_examples(kernel: sk.Kernel) -> None:
    questions = [
        "subject?",
        "genre?",
        "format?",
        "likes or dislikes?",
        "favorite actor or actress?",
    ]

    for question in questions:
        print(f"Question: {question}")
        result = await kernel.memory.search_async("preferences", question)
        print(f"Answer: {result[0].text}\n")
        
        
async def main():
    await populate_memory(kernel)
    await search_memory_examples(kernel)

# Run the event loop
asyncio.run(main())



