import json

from dotenv import load_dotenv
from openai import OpenAI

from chatter.agent_manager import BaseAgent
from chatter.chat_models import Message

load_dotenv()  # loading and setting the api key can be done in one step


class POpenAIAgent(BaseAgent):
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
        self.tools = []

    def generate_response(self):
        return self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.7,
        )

    async def get_response(self, user_input, thread_id=None):
        self.messages += [{"role": "user", "content": user_input}]
        response = self.generate_response()
        return str(response)

    def generate_response_stream(self):
        return self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.7,
            stream=True,
            tools=self.tools,
        )

    def get_response_stream(self, user_input, thread_id=None):
        self.last_message = ""
        self.messages += [{"role": "user", "content": user_input}]
        response = self.generate_response_stream()

        def generate_responses():
            tool_calls = None
            arguments = ""
            function = ""
            for message in response:
                if tool_calls:
                    if message.choices[0].delta.tool_calls:
                        args = message.choices[0].delta.tool_calls[0].function.arguments
                        arguments += str(args)
                elif message.choices[0].delta.tool_calls:
                    tool_calls = message.choices[0].delta.tool_calls
                    function = str(tool_calls[0].function.name)
                else:
                    self.last_message += message.choices[0].delta.content
                    content = message.choices[0].delta.content
                    if content:
                        self.last_message += message.choices[0].delta.content
                    yield message

            if tool_calls:
                # yield message  # this is the last message and it is closes the stream
                tool_call = tool_calls[0]
                action = [
                    action for action in self.actions if action["name"] == function
                ]
                if action and arguments and len(action) == 1:
                    action_response = action[0]["pointer"](**json.loads(arguments))
                    print(action_response)
                    self.messages.append(message)
                    self.messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function,
                            "content": action_response,
                        }
                    )
                    response2 = self.generate_response()
                    arguments = ""
                    function = ""
                    for message in response2:
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

    def load_actions(self):
        for action in self.actions:
            self.tools.append(action["agent_action"])
