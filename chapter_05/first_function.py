import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
# Ensure the API key is available
if not api_key:
    raise ValueError("No API key found. Please check your .env file.")
client = OpenAI(api_key=api_key)


# Example function to query ChatGPT
def ask_chatgpt(user_message):    
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",  # gpt-4 turbo or a model of your preference
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": user_message}],
        temperature=0.7,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "recommend",
                    "description": "Provide a recommendation for any topic.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "The topic, a user wants a recommnedation for.",
                            },
                            "rating": {
                                "type": "string",
                                "description": "The rating this recommendation was given.",
                                "enum": ["good", "bad", "terrible"]
                                },
                        },
                        "required": ["topic"],
                    },
                },
                }
            ]
        )
    return response.choices[0].message.tool_calls[0].function


# Example usage
user = "Can you please recommend me a time travel movie?"
response = ask_chatgpt(user)
print(response)

user = "Can you please recommend me a good time travel movie?"
response = ask_chatgpt(user)
print(response)