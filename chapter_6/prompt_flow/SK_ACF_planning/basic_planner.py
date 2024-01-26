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
from semantic_kernel.core_skills.math_skill import MathSkill
from semantic_kernel.core_skills.conversation_summary_skill import ConversationSummarySkill
from semantic_kernel.core_skills.time_skill import TimeSkill
from semantic_kernel.core_skills.text_skill import TextSkill
from typing import Union, List
from q_planner import QPlanner


@tool
def my_python_tool(
    input: str,
    goal_embedding: List[float],
    # semantic_function: str,
    # function_name: str,
    # skill_name: str,
    max_tokens: int,
    temperature: float,
    deployment_name: str,
    connection: Union[OpenAIConnection, AzureOpenAIConnection],
) -> str:
    # Initialize the kernel
    kernel = sk.Kernel(log=sk.NullLogger())
    
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
        
    kernel.import_skill(MathSkill(), "MathPlugin")
    kernel.import_skill(ConversationSummarySkill(kernel), "ConversationSummaryPlugin")
    kernel.import_skill(TimeSkill(), "TimePlugin")
    kernel.import_skill(TextSkill(), "TextPlugin")
                  
    planner = QPlanner()
    
    async def main():
        goal = f"{input}"         
             
        plan = await planner.create_plan_async(goal,
                                               goal_embedding,
                                               kernel,
                                               max_tokens=max_tokens,
                                               temperature=temperature) 

        print(plan.generated_plan)

        # Execute the plan
        results = await planner.execute_plan_async(plan, kernel) 
        return results, str(plan.generated_plan)
    
    # Run the event loop
    try:
        result, plan = asyncio.run(main())
        return result, plan
    except Exception as e:
        print(e)
        return ""

    


