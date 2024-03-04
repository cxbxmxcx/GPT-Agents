import importlib.util
import os


class BaseAgent:
    def __init__(self, chat_history=None):
        self._chat_history = chat_history or []
        self.last_message = ""
        self.system_message = (
            "You are a chat bot. Your goal is to figure out what people need."
        )
        # self.chat = self.initialize_chat_history(self.system_message)

    def initialize_chat_history(self, system_message):
        # Initialize chat history with the system message or any other initial setup
        chat_history = [{"role": "system", "content": system_message}]
        return chat_history

    async def get_response(self, user_input, thread_id=None):
        # Placeholder method to be implemented by subclasses
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_response_stream(self, user_input, thread_id=None):
        # Placeholder method for streaming responses, to be implemented by subclasses
        raise NotImplementedError("This method should be implemented by subclasses.")

    def append_chat_history(self, thread_id, user_input, response):
        # Method to append user input and bot response to the chat history
        self._chat_history.append(
            {"role": "user", "content": user_input, "thread_id": thread_id}
        )
        self._chat_history.append(
            {"role": "bot", "content": response, "thread_id": thread_id}
        )

    def load_chat_history(self):
        # Placeholder method to load and format chat history for the specific tool
        raise NotImplementedError("This method should be implemented by subclasses.")

    @property
    def chat_history(self):
        return self._chat_history

    # define the setter method
    @chat_history.setter
    def chat_history(self, chat_history):
        self._chat_history = chat_history
        self.load_chat_history()

    @property
    def name(self):
        # Property to get the name of the agent
        return self.__class__.__name__


class AgentManager:
    def __init__(self):
        plugin_directory = os.path.join(os.path.dirname(__file__), "agents")
        self.plugins = self._load_agent_plugins(plugin_directory)

    def get_agent(self, agent_name):
        for plugin in self.plugins:
            if plugin.name == agent_name:
                return plugin
        return None

    def get_agent_names(self):
        return [plugin.name for plugin in self.plugins]

    def _load_agent_plugins(self, plugin_directory):
        plugins = []
        for filename in os.listdir(plugin_directory):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                module_path = os.path.join(plugin_directory, filename)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if (
                        isinstance(attribute, type)
                        and issubclass(attribute, BaseAgent)
                        and attribute is not BaseAgent
                    ):
                        plugins.append(attribute())
        return plugins
