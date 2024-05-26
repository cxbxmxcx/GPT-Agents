import asyncio

import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai

# from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptTemplate
from semantic_kernel.connectors.ai.open_ai.utils import (
    chat_completion_with_tool_call,
    get_tool_call_object,
)
from semantic_kernel.contents.chat_history import ChatHistory

from plugins.Movies.tmdb import TMDbService

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

tmdb_service = kernel.import_plugin_from_object(TMDbService(), "TMDBService")

# set up the execution settings
if selected_service == "OpenAI":
    execution_settings = sk_oai.OpenAIChatPromptExecutionSettings(
        service_id=service_id,
        ai_model_id=model_id,
        max_tokens=2000,
        temperature=0.7,
        top_p=0.8,
        tool_choice="auto",
        tools=get_tool_call_object(kernel, {"exclude_plugin": ["ChatBot"]}),
    )
elif selected_service == "AzureOpenAI":
    execution_settings = sk_oai.OpenAIChatPromptExecutionSettings(
        service_id=service_id,
        ai_model_id=deployment,
        max_tokens=2000,
        temperature=0.7,
        top_p=0.8,
        tool_choice="auto",
        tools=get_tool_call_object(kernel, {"exclude_plugin": ["ChatBot"]}),
    )

# OpenAIChatPromptTemplate
# prompt_template_config = sk.PromptTemplateConfig(
#     template="{{$user_input}}",
#     name="Chat",
#     template_format="semantic-kernel",
#     input_variables=[
#         InputVariable(
#             name="user_input", description="The user input", is_required=True
#         ),
#         InputVariable(
#             name="history",
#             description="The history of the conversation",
#             is_required=True,
#             default="",
#         ),
#     ],
#     execution_settings={"default": execution_settings},
# )

prompt_config = sk.PromptTemplateConfig.from_completion_parameters(
    max_tokens=2000,
    temperature=0.7,
    top_p=0.8,
    function_call="auto",
    chat_system_prompt="You are a chat bot that recommends movies and TV Shows.",
)
prompt_template = OpenAIChatPromptTemplate(
    "{{$user_input}}", kernel.prompt_template_engine, prompt_config
)


history = ChatHistory()

history.add_system_message("You recommend movies and TV Shows.")
history.add_user_message("Hi there, who are you?")
history.add_assistant_message(
    "I am Rudy, the recommender chat bot. I'm trying to figure out what people need."
)

chat_function = kernel.create_function_from_prompt(
    prompt_template_config=prompt_template,
    plugin_name="ChatBot",
    function_name="Chat",
)


async def chat() -> bool:
    try:
        user_input = input("User:> ")
    except KeyboardInterrupt:
        print("\n\nExiting chat...")
        return False
    except EOFError:
        print("\n\nExiting chat...")
        return False

    if user_input == "exit":
        print("\n\nExiting chat...")
        return False
    arguments = sk.KernelArguments(
        user_input=user_input,
        history=("\n").join([f"{msg.role}: {msg.content}" for msg in history]),
    )
    result = await chat_completion_with_tool_call(
        kernel=kernel,
        arguments=arguments,
        chat_plugin_name="ChatBot",
        chat_function_name="Chat",
        chat_history=history,
    )
    print(f"GPT Agent:> {result}")
    return True


async def main() -> None:
    chatting = True
    print(
        "Welcome to the chat bot!\
\n  Type 'exit' to exit.\
\n  Try a math question to see the function calling in action (i.e. what is 3+3?)."
    )
    while chatting:
        chatting = await chat()


if __name__ == "__main__":
    asyncio.run(main())
