from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()  # loading and setting the api key can be done in one step
client = OpenAI()


# Example function to query ChatGPT
def ask_chatgpt(messages):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        temperature=0.7,   
        response_format={"type": "json_object"},     
        )       
    
    return response.choices[0].message.content


messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant and always output JSON."  
        },
    {
        "role": "user",
        "content": "What is the captial of France?"
        },
    {
        "role": "assistant",
        "content": "The capital of France is Paris."
        },
    {
        "role": "user",
        "content": "What is an interesting fact of Paris."
        }
    ]
response = ask_chatgpt(messages)
print(response)
