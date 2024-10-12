from promptflow import tool
from typing import List


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(experts_text: str) -> List[str]:
    sections = experts_text.split('<')
    
    # Initialize a dictionary to hold the steps for each expert
    expert_steps = []

    # Process each section
    for section in sections:
        if section.startswith('expert'):
            # Extract the expert number and the associated text
            expert_number, expert_text = section.split('>\n', 1)
            
            # Further split the text into lines and remove empty lines
            lines = [line.strip() for line in expert_text.split('\n') if line.strip()]
            
            # Store the steps in the dictionary under the respective expert
            expert_steps.append(lines)

    return expert_steps

    
