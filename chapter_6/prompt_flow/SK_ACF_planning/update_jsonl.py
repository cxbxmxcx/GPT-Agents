from promptflow import tool
import json
from typing import List


@tool
def write_to_jsonl(
        problems: List[str],
        expected: List[str],
        predicted: List[str],
        evaluations: List[str],
        feedbacks: List[str],
        deployment_names: List[str],
        output_file: str) -> None:
    """
    Writes data from six lists into a JSON lines file, adhering to a maximum
    line length for better readability.

    Parameters:
    - problems: List of problems.
    - expected: List of expected outcomes.
    - predicted: List of predicted outcomes.
    - evaluations: List of evaluations.
    - feedbacks: List of feedbacks.
    - deployment_names: List of deployment names.    
    - output_file: File path for the output JSON lines file.
    """
    # Ensure all lists are of the same length
    if not len(problems) == len(expected) == len(predicted) \
       == len(evaluations) == len(feedbacks) == len(deployment_names):
        raise ValueError("All lists must be of the same length.")
    
    with open(output_file, 'w') as file:
        for values in zip(problems, expected, predicted, evaluations,
                          feedbacks, deployment_names):
            record = {
                "problem": values[0],
                "expected": values[1],
                "predicted": values[2],
                "evaluation": values[3],
                "feedback": values[4],
                "deployment_name": values[5]
            }
            json_line = json.dumps(record)
            file.write(json_line + '\n')

