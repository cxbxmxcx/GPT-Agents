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
from semantic_kernel.planning import (    
    StepwisePlanner,
    )
from semantic_kernel.planning.stepwise_planner.stepwise_planner_config import (
    StepwisePlannerConfig,
)
from semantic_kernel.core_skills.math_skill import MathSkill
from semantic_kernel.core_skills.conversation_summary_skill import ConversationSummarySkill
from semantic_kernel.core_skills.time_skill import TimeSkill
from semantic_kernel.core_skills.text_skill import TextSkill
from typing import Union, List


@tool
def my_python_tool(
    input: str,
    # semantic_function: str,
    # function_name: str,
    # skill_name: str,
    # max_tokens: int,
    # temperature: float,
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
                  
    planner = StepwisePlanner(kernel, StepwisePlannerConfig(max_iterations=10, min_iteration_time_ms=1000))
    
    async def main():
        goal = f"{input}"        
        plan = planner.create_plan(goal=goal) 

        # Execute the plan
        # results = await planner.execute_plan_async(plan) 
        result = await plan.invoke_async()
        
        #output the executed plan
        for index, step in enumerate(plan._steps):
            print("Step:", index)
            print("Description:", step.description)
            print("Function:", step.name + "." + step._function.name)
            if len(step._outputs) > 0:
                print("  Output:\n", str.replace(result[step._outputs[0]], "\n", "\n  "))
        return result
    
    # Run the event loop
    try:
        result = asyncio.run(main()).result
        return result
    except Exception as e:
        print(e)
        return ""

    


