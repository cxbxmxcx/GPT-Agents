from chatter.action_manager import agent_action


@agent_action
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    return f"The current weather in {location} is 45{unit}."


# Example usage for a semantic action
@agent_action
def recommend(topic):
    """Provide a recommendation for a given {{topic}}."""
    return __doc__
