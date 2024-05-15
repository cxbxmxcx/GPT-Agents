import gradio as gr
from openai import OpenAI

from dotenv import load_dotenv
from gradio_assistants_panel import assistants_panel
from assistants_utils import EventHandler
from assistants_api import api


load_dotenv()
client = OpenAI()      
            
thread = client.beta.threads.create()  # create a new thread everytime this is run

# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.


def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)
       
def ask_assistant(history, message):
    if history is None:
        history = []
    for file in message["files"]:
        history.append(((file,), None))
        # upload files to the thread
    if message["text"] is not None:
        history.append((message["text"], None))
        msg = message["text"]
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=msg
    )
    return history, gr.MultimodalTextbox(value=None, interactive=False)
  
def run(history, assistant_id): 
    assistant = api.retrieve_assistant(assistant_id)
    if assistant is None:
        msg = "Assistant not found."
        history.append((None, msg))
        yield history, msg
        return
    
    eh = EventHandler() 
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,   
        event_handler=eh,   
    ) as stream:   
        while len(eh.images) > 0:  
            history.append((None, (eh.images.pop(),))) 
            history.append(("", None))         
        history[-1][1] = "" 
        for text in stream.text_deltas:
            history[-1][1] += text
            yield history, "".join(eh.logs) 
            
    while len(eh.images) > 0:
        history.append((None, (eh.images.pop(),))) 
        yield history, "".join(eh.logs)
    
        
custom_css = """
:root {
    --adjustment-ratio: 150px; /* Height to subtract from the viewport for chatbot */
}

body, html {
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
}

.gradio-container {
    max-width: 100% !important; 
    width: 100%;
}

#chatbot {
    height: calc(100vh - var(--adjustment-ratio)) !important; /* Uses adjustment ratio */
    overflow-y: auto !important;
}

#instructions textarea {
    min-height: calc(100vh - (var(--adjustment-ratio) + 800px)); /* Additional subtraction to account for other elements */
    max-height: 1000px;
    resize: vertical;
    overflow-y: auto;
}
#assistant_logs textarea {
    min-height: calc(100vh - (var(--adjustment-ratio) - 25px)); /* Additional subtraction to account for other elements */
    max-height: 1000px;
    resize: vertical;
    overflow-y: auto;
}
"""

with gr.Blocks(css=custom_css) as demo:
    assistant_logs = gr.TextArea(label="Assistant Logs", placeholder="Logs here...", elem_id="assistant_logs", interactive=False, render=False)
    with gr.Row():
        with gr.Column(scale=2): 
            assistant_id = assistants_panel()
            
        with gr.Column(scale=8):
            chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                bubble_full_width=True,
                container=True,
                avatar_images=["avatar1.png", "avatar2.png"],
                layout="panel" 
            )

            chat_input = gr.MultimodalTextbox(interactive=True, file_types=["image"], placeholder="Enter message or upload file...", show_label=False, elem_id="chat_input")

            chat_msg = chat_input.submit(ask_assistant, [chatbot, chat_input], [chatbot, chat_input])
            bot_msg = chat_msg.then(run, [chatbot, assistant_id], [chatbot, assistant_logs], api_name="assistant_response")
            bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

            chatbot.like(print_like_dislike, None, None)
        with gr.Column(scale=2):
            assistant_logs.render()

demo.queue()


if __name__ == "__main__":
    demo.launch()