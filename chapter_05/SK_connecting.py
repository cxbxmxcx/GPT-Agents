from semantic_kernel import Kernel
from service_settings import ServiceSettings
from services import Service
import asyncio

async def run_prompt():
    result = await kernel.invoke_prompt(prompt="recommend a movie about time travel")
    print(result)

kernel = Kernel()
service_settings = ServiceSettings.create()
selectedService = (
    Service.OpenAI
    if service_settings.global_llm_service is None
    else Service(service_settings.global_llm_service.lower())
)
service_id = None
if selectedService == Service.OpenAI:
    from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

    service_id = "default"
    kernel.add_service(
        OpenAIChatCompletion(
            service_id=service_id,
        ),
    )
elif selectedService == Service.AzureOpenAI:
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

    service_id = "default"
    kernel.add_service(
        AzureChatCompletion(
            service_id=service_id,
        ),
    )

asyncio.run(run_prompt())
