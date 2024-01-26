import asyncio
from promptflow import tool
import semantic_kernel as sk
from promptflow.connections import (
    AzureOpenAIConnection,
    OpenAIConnection,
)
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatCompletion,
)
from typing import Union, List

@tool
def my_python_tool(
    input: str,
    input_node: int,
    history: str,
    semantic_function: str,
    function_name: str,
    skill_name: str,
    max_tokens: int,
    temperature: float,
    deployment_name: str,
    connection: Union[OpenAIConnection, AzureOpenAIConnection],
) -> str:
    # Initialize the kernel
    kernel = sk.Kernel(log=sk.NullLogger())
    
    if isinstance(input, List):
        input = input[input_node] 
        if isinstance(input, List):
            input = "\n".join(input)
    
    if isinstance(connection, AzureOpenAIConnection):
        chat = AzureChatCompletion(
            deployment_name,
            connection.api_base,
            connection.api_key,           
        )
        kernel.add_chat_service("chat_completion", chat)
    elif isinstance(connection, OpenAIConnection):
        chat = OpenAIChatCompletion(
            ai_model_id=deployment_name,
            api_key=connection.api_key,                    
        )  
        kernel.add_chat_service("chat-gpt", chat)        
          
    function = kernel.create_semantic_function(semantic_function,
                                               function_name=function_name,
                                               skill_name=skill_name,
                                               max_tokens=max_tokens,
                                               temperature=temperature,
                                               top_p=0.5)

    async def main():
        query = f"{history}\n{input}"
        return await function.invoke_async(query)        

    # Run the event loop
    result = asyncio.run(main()).result

    return result


