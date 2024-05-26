import datetime

import openai
from dotenv import load_dotenv
from openai import AssistantEventHandler
from typing_extensions import override

load_dotenv()

# OpenAI client initialization
client = openai.OpenAI()


def save_binary_response_content(binary_content):
    # Function to get the current timestamp
    def get_timestamp():
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Function to determine the file extension based on the magic numbers (file signatures)
    def get_file_extension(byte_string):
        if byte_string.startswith(b"\x89PNG\r\n\x1a\n"):
            return "png"
        elif byte_string.startswith(b"\xff\xd8\xff\xe0") or byte_string.startswith(
            b"\xff\xd8\xff\xe1"
        ):
            return "jpg"
        elif byte_string.startswith(b"GIF87a") or byte_string.startswith(b"GIF89a"):
            return "gif"
        elif byte_string.startswith(b"%PDF-"):
            return "pdf"
        # Add more signatures as needed
        else:
            return "bin"  # Generic binary file extension

    # Get the file extension
    extension = get_file_extension(binary_content)

    # Create a unique file name using the timestamp
    timestamp = get_timestamp()
    file_name = f"file_{timestamp}.{extension}"

    # Save the content to the file
    with open(file_name, "wb") as file:
        file.write(binary_content)
        print(f"File saved as {file_name}")

    return file_name


class EventHandler(AssistantEventHandler):
    def __init__(self, logs) -> None:
        super().__init__()
        self._logs = logs
        self._images = []

    @property
    def logs(self):
        return self._logs

    @property
    def images(self):
        return self._images

    @override
    def on_text_created(self, text) -> None:
        print("assistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        # print(delta.value, flush=True)
        if delta.annotations:
            print(delta.annotations, end="", flush=True)

    def on_image_file_done(self, image_file) -> None:
        print(image_file, end="", flush=True)
        content = client.files.content(image_file.file_id)
        image_file = save_binary_response_content(content.content)
        self._logs += [f"File saved as {image_file}"]
        self._images += [image_file]

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)
        self._logs += [f"\nassistant > {tool_call.type}"]
        if tool_call.type == "code_interpreter":
            self._logs += ["\n```python"]

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
                self._logs += [f"{delta.code_interpreter.input}"]
        if delta.code_interpreter.outputs:
            print("\noutput >", flush=True)
            for output in delta.code_interpreter.outputs:
                if output.type == "logs":
                    print(f"{output.logs}", flush=True)
                    self._logs += [f"{output.logs}"]

    def on_tool_call_done(self, tool_call) -> None:
        if tool_call.type == "code_interpreter":
            self._logs += ["\n```\n"]
