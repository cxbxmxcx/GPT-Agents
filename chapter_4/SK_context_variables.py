import asyncio

import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.prompt_template.input_variable import InputVariable

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

prompt = """
system:

You have vast knowledge of everything and can recommend anything provided you are given the following criteria, the subject, genre, format and any other custom information.

user:
Please recommend a {{$format}} with the subject {{$subject}} and {{$genre}}. 
Include the following custom information: {{$custom}}
"""

prompt_template_config = sk.PromptTemplateConfig(
    template=prompt,
    name="tldr",
    template_format="semantic-kernel",
    input_variables=[
        InputVariable(
            name="format", description="The format to recommend", is_required=True
        ),
        InputVariable(
            name="suject", description="The subject to recommend", is_required=True
        ),
        InputVariable(
            name="genre", description="The genre to recommend", is_required=True
        ),
        InputVariable(
            name="custom",
            description="Any custom information to enhance the recommendation",
            is_required=True,
        ),
    ],
    execution_settings=execution_settings,
)

recommend_function = kernel.create_function_from_prompt(
    prompt_template_config=prompt_template_config,
    function_name="Recommend_Movies",
    plugin_name="Recommendation",
)


async def run_recommendation(
    subject="time travel", format="movie", genre="medieval", custom="must be a comedy"
):
    recommendation = await kernel.invoke(
        recommend_function,
        sk.KernelArguments(subject=subject, format=format, genre=genre, custom=custom),
    )
    print(recommendation)


# Use asyncio.run to execute the async function
asyncio.run(run_recommendation())
