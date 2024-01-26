
from typing import List
from promptflow import tool
from q_planner import SemanticMemory

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(
    plan: str,
    goal_embedding: List[float],
    q_value: str,
) -> str:
    sm = SemanticMemory()
    sm.update_memory(goal_embedding, plan[1], q_value)
    sm.save_memory()
    return "Success"
    
