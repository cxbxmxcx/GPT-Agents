import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.prompt_template.input_variable import InputVariable
from semantic_kernel.prompt_template.prompt_template_config import PromptTemplateConfig

from chatter.agent_plugins import BaseAgent
from chatter.utils import async_to_sync_generator


class SKAgent(BaseAgent):
    def __init__(self, chat_history=None):
        system_message = """
        You are a chat bot. Your name is Mosscap and
        you have one goal: figure out what people need.
        Your full name, should you need to know it, is
        Splendid Speckled Mosscap. You communicate
        effectively, but you tend to answer with long
        flowery prose.
        """
        template = """
        {{$chat_history}}
        
        user:
        {{$user_input}}
        """
        self.last_message = ""
        self._chat_history = chat_history
        self.kernel = sk.Kernel()
        service_id = "chat-gpt"
        api_key, org_id = sk.openai_settings_from_dot_env()
        self.kernel.add_service(
            sk_oai.OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id="gpt-4-1106-preview",
                api_key=api_key,
                org_id=org_id,
            )
        )

        req_settings = self.kernel.get_service(
            service_id
        ).get_prompt_execution_settings_class()(service_id=service_id)
        req_settings.max_tokens = 2000
        req_settings.temperature = 0.7
        req_settings.top_p = 0.8

        prompt_template_config = PromptTemplateConfig(
            template=template,
            name="chat",
            template_format="semantic-kernel",
            input_variables=[
                InputVariable(
                    name="user_input",
                    description="The user input",
                    is_required=True,
                    default="",
                ),
                InputVariable(
                    name="chat_history",
                    description="The history of the conversation",
                    is_required=True,
                ),
            ],
            execution_settings=req_settings,
        )

        self.chat = ChatHistory(system_message=system_message)
        self.chat_function = self.kernel.create_function_from_prompt(
            plugin_name="ChatBot",
            function_name="Chat",
            prompt_template_config=prompt_template_config,
        )
        # self._load_chat_history()

    async def get_response(self, user_input, thread_id=None):
        answer = await self.kernel.invoke(
            self.chat_function,
            KernelArguments(user_input=user_input, chat_history=self.chat),
        )
        self.append_chat_history(thread_id, user_input, str(answer))
        return str(answer)

    def get_response_stream(self, user_input, thread_id=None):
        stream = self.kernel.invoke_stream(
            self.chat_function,
            KernelArguments(user_input=user_input, chat_history=self.chat),
        )
        self.last_message = ""

        async def stream_to_generator(stream):
            async for item in stream:
                el = item[0]
                c = el.content
                if c:
                    self.last_message += c
                yield el.content
                # yield item

        generator = stream_to_generator(stream)

        return async_to_sync_generator(generator)

    def load_chat_history(self):
        if self.chat_history:
            for message in self.chat_history:
                if message.role == "user":
                    self.chat.add_user_message(message.content)
                else:
                    self.chat.add_assistant_message(message.content)
