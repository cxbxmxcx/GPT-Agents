from promptflow import tool


@tool
def line_process(recommendations: str):
    """
    This tool processes the recommendation of a single line and returns the avg_score.

    :param recommendation: the set of recommendations from a single line.
    
    """    
    inputs = recommendations   
    output = []
    for data_dict in inputs:
        # Calculating the total score and average
        total_score = 0
        score_count = 0

        for key, value in data_dict.items():
                if key != "title":  # Exclude the title from scoring 
                    try:                           
                        total_score += float(value)
                        score_count += 1
                        data_dict[key] = float(value)
                    except:
                        pass
                
        avg_score = total_score / score_count if score_count > 0 else 0

        data_dict["avg_score"] = round(avg_score, 2)
        output.append(data_dict)
    
    return output