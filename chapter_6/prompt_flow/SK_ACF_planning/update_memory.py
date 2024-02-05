import asyncio
import uuid
from promptflow import tool
import semantic_kernel as sk
from promptflow.connections import (
    AzureOpenAIConnection,
    OpenAIConnection,
)
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAITextEmbedding,
    AzureChatCompletion,
    AzureTextEmbedding,
)
from semantic_kernel.connectors.memory.chroma.chroma_memory_store import ChromaMemoryStore
from typing import Union, List


@tool
def my_python_tool(
    feedback: str,
    goal: str,
    max_tokens: int,
    temperature: float,
    deployment_name: str,
    connection: Union[OpenAIConnection, AzureOpenAIConnection],
) -> str:
    # Initialize the kernel
    kernel = sk.Kernel(log=sk.NullLogger())
    
    if isinstance(connection, AzureOpenAIConnection):
        chat = AzureChatCompletion(
            deployment_name=deployment_name,
            endpoint=connection.api_base,
            api_key=connection.api_key,           
        )
        kernel.add_chat_service("chat_completion", chat)
        azure_text_embedding = AzureTextEmbedding(deployment_name="text-embedding",
                                                  endpoint=connection.api_base,
                                                  api_key=connection.api_key)
        kernel.add_text_embedding_generation_service("ada", azure_text_embedding)
    elif isinstance(connection, OpenAIConnection):
        chat = OpenAIChatCompletion(
            ai_model_id=deployment_name,
            api_key=connection.api_key, 
        )  
        kernel.add_chat_service("chat-gpt", chat)
        oai_text_embedding = OpenAITextEmbedding(ai_model_id="text-embedding-ada-002",
                                                 api_key=connection.api_key,
                                                 )        
        kernel.add_text_embedding_generation_service("ada", oai_text_embedding)
        
    # Add memory to the kernel
    kernel.register_memory_store(memory_store=ChromaMemoryStore())
    kernel.import_skill(sk.core_skills.TextMemorySkill())
    
    async def add_feedback():        
        # Add feedback to the semantic memory        
        id = str(uuid.uuid4())
        await kernel.memory.save_information_async(collection="acf",
                                             id=id,
                                             text=goal)
    
    # Run the event loop
    try:
        result = asyncio.run(add_feedback())
        return result
    except Exception as e:
        print(e)
        raise   
    
    
    
    
