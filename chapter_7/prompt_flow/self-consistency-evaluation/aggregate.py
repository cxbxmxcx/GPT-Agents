from typing import List
from promptflow import tool


@tool
def aggregate(processed_results: List[str]):
    """
    This tool aggregates the processed result of all lines and log metric.

    :param processed_results: List of the output of line_process node.
    """

    # Add your aggregation logic here

    aggregated_results = {}

    # Log metric
    # from promptflow import log_metric
    # log_metric(key="<my-metric-name>", value=aggregated_results["<my-metric-name>"])

    return aggregated_results
