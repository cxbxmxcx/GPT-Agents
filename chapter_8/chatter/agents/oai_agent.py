from dotenv import load_dotenv
from openai import OpenAI

from chatter.agent_plugins import BaseAgent
from chatter.chat_models import Message

load_dotenv()  # loading and setting the api key can be done in one step


class OpenAIAgent(BaseAgent):
    def __init__(self, chat_history=None):
        system_message = """
        You are a chat bot. Your name is Olly the OpenAI agent and
        you have one goal: figure out what people need.
        You communicate effectively and are very terse.
        """
        template = """
        {{$chat_history}}
        
        user:
        {{$user_input}}
        """
        self.last_message = ""
        self._chat_history = chat_history
        self.client = OpenAI()
        self.model = "gpt-4-1106-preview"
        self.temperature = 0.7
        self.messages = []  # history of messages

    async def get_response(self, user_input, thread_id=None):
        self.messages += [{"role": "user", "content": user_input}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.7,
        )

        return str(response)

    def get_response_stream(self, user_input, thread_id=None):
        self.last_message = ""
        self.messages += [{"role": "user", "content": user_input}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.7,
            stream=True,
        )

        def generate_responses():
            for message in response:
                content = message.choices[0].delta.content
                if content:
                    self.last_message += message.choices[0].delta.content
                yield message

        return generate_responses

    def append_message(self, message: Message):
        if message.role == "agent":
            self.messages.append(dict(role="assistant", content=message.content))
        else:
            self.messages.append(dict(role=message.role, content=message.content))

    def load_chat_history(self):
        if self.chat_history:
            for message in self.chat_history:
                self.append_message(message)
