# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
from typing import Tuple

import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.connectors.ai.open_ai.semantic_functions.open_ai_chat_prompt_template import (
    OpenAIChatPromptTemplate,
)
from semantic_kernel.connectors.ai.open_ai.utils import (
    chat_completion_with_function_call,
    get_function_calling_object,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
#from skills.Movies.tmdb import TMDbService
from skills.Movies.tmdb_v2 import TMDbService

system_message = "You are a helpful AI assistant."

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


kernel.import_skill(TMDbService(), skill_name="TMDbService")

# enabling or disabling function calling is done by setting the function_call parameter for the completion.
# when the function_call parameter is set to "auto" the model will decide which function to use, if any.
# if you only want to use a specific function, set the name of that function in this parameter,
# the format for that is 'SkillName-FunctionName', (i.e. 'math-Add').
# if the model or api version do not support this you will get an error.
prompt_config = sk.PromptTemplateConfig.from_completion_parameters(
    max_tokens=2000,
    temperature=0.7,
    top_p=0.8,
    function_call="auto",
    chat_system_prompt=system_message,
)
prompt_template = OpenAIChatPromptTemplate(
    "{{$user_input}}", kernel.prompt_template_engine, prompt_config
)

function_config = sk.SemanticFunctionConfig(prompt_config, prompt_template)
chat_function = kernel.register_semantic_function("ChatBot", "Chat", function_config)

# calling the chat, you could add a overloaded version of the settings here,
# to enable or disable function calling or set the function calling to a specific skill.
# see the openai_function_calling example for how to use this with a unrelated function definition
filter = {"exclude_skill": ["ChatBot"]}
functions = get_function_calling_object(kernel, filter)


async def chat(context: sk.SKContext) -> Tuple[bool, sk.SKContext]:
    try:
        user_input = input("User:> ")
        context.variables["user_input"] = user_input
    except KeyboardInterrupt:
        print("\n\nExiting chat...")
        return False, None
    except EOFError:
        print("\n\nExiting chat...")
        return False, None

    if user_input == "exit":
        print("\n\nExiting chat...")
        return False, None

    context = await chat_completion_with_function_call(
        kernel,
        chat_skill_name="ChatBot",
        chat_function_name="Chat",
        context=context,
        functions=functions,
    )
    print(f"Agent:> {context.result}")
    return True, context


async def main() -> None:
    chatting = True
    context = kernel.create_new_context()
    
    print(
        "Welcome to your first GPT Agent\
\n  Type 'exit' to exit.\
\n  Ask to get a list of currently playing movies by genre."
    )
    while chatting:
        chatting, context = await chat(context)


if __name__ == "__main__":
    asyncio.run(main())