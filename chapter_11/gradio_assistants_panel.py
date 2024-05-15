import gradio as gr
from assistants_api import api

def assistants_panel():
    # Get the list of assistants
    assistant_choices = api.list_assistants()
    assistant_options = {a.name: a.id for a in assistant_choices.data}
    assistant_options['Create New Assistant'] = 'new'
    # assistant_choices.append("Create New Assistant")
    assistant_selected = gr.Dropdown(label="Select Assistant", choices=assistant_options,  interactive=True, )
    
    def get_assistant_details(assistant_key):
        if assistant_key == 'new':
            return '', '', '', 'gpt-4o', [], '', 'JSON object', 1, 1
        else:
            # Replace with the actual code to get the assistant details based on the assistant ID
            return 'Assistant Name', assistant_options[assistant_key], 'You are a helpful assistant.', 'gpt-4o', ['File search'], '', 'JSON object', 1, 1

    def assistant_selected_change(assistant_key):
        if assistant_key == 'new':
            return gr.update(visible=True), gr.update(visible=False)
        else:
            return gr.update(visible=False), gr.update(visible=True)
        
    with gr.Column(visible=False) as new_assistant_form:
        assistant_name_new = gr.Textbox(label="Enter a user-friendly name", placeholder="Enter Name")
        assistant_instructions_new = gr.Textbox(label="Instructions", placeholder="You are a helpful assistant.", elem_id="instructions")
        assistant_model_new = gr.Dropdown(label="Model", choices=["gpt-3", "gpt-3.5", "gpt-4", "gpt-4o"], value="gpt-4o")
        assistant_tools_new = gr.CheckboxGroup(label="Tools", choices=["File search", "Code interpreter"])
        assistant_files_new = gr.Textbox(label="Add Files or Functions", placeholder="+ Files, + Functions")
        assistant_resformat_new = gr.Radio(label="Response Format", choices=["JSON object", "Plain text"], value="JSON object")
        assistant_temperature_new = gr.Slider(label="Temperature", minimum=0, maximum=1, step=0.01, value=1)
        assistant_top_p_new = gr.Slider(label="Top P", minimum=0, maximum=1, step=0.01, value=1)
        add_button = gr.Button("Add Assistant")

    with gr.Column() as existing_assistant_form:   
        assistant_id = gr.Markdown("")      
        assistant_name = gr.Textbox(label="Enter a user-friendly name", placeholder="Enter Name") 
        assistant_instructions = gr.Textbox(label="Instructions", placeholder="You are a helpful assistant.", elem_id="instructions")
        assistant_model = gr.Dropdown(label="Model", choices=["gpt-3", "gpt-3.5", "gpt-4", "gpt-4o"], value="gpt-4o")
        assistant_tools = gr.CheckboxGroup(label="Tools", choices=["File search", "Code interpreter"])
        assistant_files = gr.Textbox(label="Add Files or Functions", placeholder="+ Files, + Functions")
        assistant_resformat = gr.Radio(label="Response Format", choices=["JSON object", "Plain text"], value="JSON object")
        assistant_temperature = gr.Slider(label="Temperature", minimum=0, maximum=1, step=0.01, value=1)
        assistant_top_p = gr.Slider(label="Top P", minimum=0, maximum=1, step=0.01, value=1)
        delete_button = gr.Button("🗑️")

    assistant_selected.change(
        fn=lambda x: get_assistant_details(x),
        inputs=assistant_selected,
        outputs=[assistant_name, assistant_id, assistant_instructions, assistant_model, assistant_tools, assistant_files, assistant_resformat, assistant_temperature, assistant_top_p]
    )
    
    assistant_selected.change(
        assistant_selected_change, 
        inputs=assistant_selected, 
        outputs=[new_assistant_form, existing_assistant_form]
    )
    
    assistant_selected.change(
        api.update_assistant,         
        inputs=[assistant_name, assistant_id, assistant_instructions, assistant_model, assistant_tools, assistant_files, assistant_resformat, assistant_temperature, assistant_top_p]
    )
    
    
    add_button.click(
        api.create_assistant,         
        inputs=[assistant_name_new, assistant_instructions_new, assistant_model_new, assistant_tools_new, assistant_files_new, assistant_resformat_new, assistant_temperature_new, assistant_top_p_new]
    )
    delete_button.click(api.delete_assistant, inputs=assistant_id)
    
    return assistant_id


