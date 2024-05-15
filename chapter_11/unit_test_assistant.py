import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from openai import OpenAI


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, assistant, thread):
        self.assistant = assistant
        self.thread = thread
        self.last_modified_time = {}
        self.debounce_period = 1  # in seconds, adjust as needed

    def on_modified(self, event):
        if not event.is_directory and event.event_type == 'modified':
            current_time = time.time()
            last_modified = self.last_modified_time.get(event.src_path, 0)

            if current_time - last_modified > self.debounce_period:
                print(f"Detected change in: {event.src_path}")
                self.process_file(event.src_path)
                self.last_modified_time[event.src_path] = current_time

    def process_file(self, file_path):
        file = client.files.create(
            file=open(file_path, "rb"),
            purpose='assistants'
            )
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="Please address the user as Jane Doe. The user has a premium account.",
            additional_messages=[
                {
                    "role": "user",
                    "content": "Create unit tests for this Python script.",
                    "attachments": [
                        {
                            "file_id": file.id,
                            "tools": [{"type": "code_interpreter"}]
                            }
                        ]
                    }
                ]
            )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            print(messages)
        else:
            print(run.status)
        # with open(file_path, 'rb') as file:
        #     files = {'file': (os.path.basename(file_path), file)}
        #     response = requests.post(self.endpoint, files=files)
        #     if response.status_code == 200:
        #         print(f"Unit tests generated for {file_path}")
        #         self.save_unit_tests(response.content, file_path)
        #     else:
        #         print("Failed to generate unit tests")

    def save_unit_tests(self, unit_tests, original_file_path):
        test_file_path = f"{original_file_path}_tests.py"
        with open(test_file_path, 'wb') as file:
            file.write(unit_tests)
        print(f"Saved unit tests to {test_file_path}")

if __name__ == "__main__":
    path = "."
    
    client = OpenAI()

    assistant = client.beta.assistants.create(
        name="Sample Assistant",
        instructions="""
            The Python Test Builder is inspired by Robert C. Martin's principles, emphasizing clarity, precision, and mentorship.
            It assists Python developers by automatically generating and running unit tests on uploaded Python scripts.
            The GPT focuses on comprehensive testing, considering all parameters and mocking out external or unknown code as necessary.
            It provides detailed listings of the tests performed, including results and any errors found. 
            The interaction style is knowledgeable yet approachable, aimed at guiding developers towards best practices in software testing.
            Never modify or suggest to modify the original code. Always just provide the file with the unit tests and nothing else.
        """,
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-turbo"
    )
    thread = client.beta.threads.create()

    event_handler = FileChangeHandler(assistant, thread)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print("Monitoring started on directory:", path)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
