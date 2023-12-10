from typing import List
from promptflow import tool
from promptflow import log_metric

@tool
def aggregate(processed_results: List[str]):
    """
    This tool aggregates the processed result of all lines and log metric.

    :param processed_results: List of the output of line_process node.
    """

    items = [item for sublist in processed_results for item in sublist]
    
    aggregated = {}

    # Iterate through each dictionary in the list
    for item in items:
        for key, value in item.items():
            # Skip the key 'title'
            if key == 'title':
                continue

            # Check if the value is a float and aggregate it
            if isinstance(value, (float, int)):
                if key in aggregated:
                    aggregated[key] += value
                else:
                    aggregated[key] = value   
                    
    # Log metric
    for key, value in aggregated.items():
        value = value / len(items)
        log_metric(key=key, value=value)
        aggregated[key] = value
        
    return aggregated

