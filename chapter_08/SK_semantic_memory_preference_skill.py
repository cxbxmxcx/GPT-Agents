import asyncio
from typing import Tuple
import uuid
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
preferences = kernel.create_semantic_function("""
You are preferences detector. 
You are able to extract a users perferences from a conversation history. 
Extract any new preferences in a comma seperated list of statements.
[INPUT]
{{$input}}
[END INPUT]
""")

async def populate_memory(kernel: sk.Kernel) -> None:
    # Add some documents to the semantic memory
    await kernel.memory.save_information_async(
        collection="preferences", id="info1", text="My subject preference is time travel "
    )
    await kernel.memory.save_information_async(
        collection="preferences", id="info2", text="My genre preference is science fiction"
    )
    await kernel.memory.save_information_async(
       collection= "preferences", id="info3", text="my format preference is TV shows"
    )
    await kernel.memory.save_information_async(
        collection="preferences", id="info4", text="I dislike old movies (before 1960)"
    )
    await kernel.memory.save_information_async(
        collection="preferences", id="info5", text="My favorite actor is Chris Pine"
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
        
        

async def setup_chat_with_memory(
    kernel: sk.Kernel,
) -> Tuple[sk.SKFunctionBase, sk.SKContext]:
    sk_prompt = """
    ChatBot can have a conversation with you about any topic.
    It can give explicit instructions or say 'I don't know' if
    it does not have an answer.

    Information about me, from previous conversations:
    - {{$preference1}} {{recall $preference1}}
    - {{$preference2}} {{recall $preference2}}
    - {{$preference3}} {{recall $preference3}}
    - {{$preference4}} {{recall $preference4}}
    - {{$preference5}} {{recall $preference5}}

    Chat:
    {{$chat_history}}
    User: {{$user_input}}
    ChatBot: """.strip()

    chat_func = kernel.create_semantic_function(sk_prompt, max_tokens=200, temperature=0.8)

    context = kernel.create_new_context()
    context["preference1"] = "subject?"
    context["preference2"] = "genre?"
    context["preference3"] = "format?"
    context["preference4"] = "likes or dislikes?"
    context["preference5"] = "favorite actor or actress?"

    context[sk.core_skills.TextMemorySkill.COLLECTION_PARAM] = "preferences"
    context[sk.core_skills.TextMemorySkill.RELEVANCE_PARAM] = "0.8"

    context["chat_history"] = ""

    return chat_func, context


async def chat(kernel: sk.Kernel,
               chat_func: sk.SKFunctionBase,
               context: sk.SKContext) -> bool:
    try:
        user_input = input("User:> ")
        context["user_input"] = user_input        
    except KeyboardInterrupt:
        print("\n\nExiting chat...")
        return False
    except EOFError:
        print("\n\nExiting chat...")
        return False

    if user_input == "exit":
        print("\n\nExiting chat...")
        return False

    answer = await kernel.run_async(chat_func, input_vars=context.variables)
    context["chat_history"] += f"\nUser:> {user_input}\nChatBot:> {answer}\n"
    new_preferences = await preferences.invoke_async(f"{user_input} {answer}")
    for pref in new_preferences.result.split(","):
        pref = pref.strip()
        if pref:
            await kernel.memory.save_information_async(
                collection="preferences",
                id=f"{uuid.uuid4()}",
                text=pref
            )    
    print(f"ChatBot:> {answer}")
    return True

        
async def main():  
    await populate_memory(kernel)    

    print("Setting up a chat (with memory!)")
    chat_func, context = await setup_chat_with_memory(kernel)

    print("Begin chatting (type 'exit' to exit):\n")
    chatting = True
    while chatting:
        chatting = await chat(kernel, chat_func, context)
        
        await search_memory_examples(kernel)
        

# Run the event loop
asyncio.run(main())


