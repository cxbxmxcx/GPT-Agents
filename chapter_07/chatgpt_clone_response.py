import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.title("ChatGPT-like clone")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What do you need?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Use st.spinner to indicate a long-running process
    with st.spinner(text="The assistant is thinking..."):
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            response_content = response.choices[0].message.content
            response = st.markdown(response_content, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": response_content})
