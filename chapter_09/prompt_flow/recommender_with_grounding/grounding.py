from promptflow import tool
from typing import List

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

# In Python tool you can do things like calling external services or
# pre/post processing of data, pretty much anything you want


@tool
def grounding(inputs: List[dict]) -> str:
    
    output = []
    for data_dict in inputs:
        # Calculating the total score and average
        total_score = 0
        score_count = 0

        for key, value in data_dict.items():
            if key != "title":  # Exclude the title from scoring            
                total_score += int(value)
                score_count += 1
                
        avg_score = total_score / score_count if score_count > 0 else 0

        data_dict["avg_score"] = round(avg_score, 2)
        output.append(data_dict)
    
    return output







