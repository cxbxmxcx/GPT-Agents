import time

import streamlit as st
from streamlit_js_eval import set_cookie

from chatter.agents.sk_agent import SKAgent
from chatter.chat_system import ChatSystem


def chat_page(username):
    chat = ChatSystem()
    user = chat.get_participant(username)
    st.set_page_config(layout="wide")

    # Initialize session state for threads and current_thread_id if not already present
    if "threads" not in st.session_state:
        threads = chat.get_threads_for_user(username)
        st.session_state["threads"] = threads
    if "current_thread_id" not in st.session_state:
        st.session_state["current_thread_id"] = None

    def select_thread(thread_id):
        st.session_state["current_thread_id"] = thread_id
        thread_history = chat.read_messages(thread_id)
        # Here, we find the thread by ID and set its 'agent' attribute
        for thread in st.session_state["threads"]:
            if thread.thread_id == thread_id:
                thread.agent = SKAgent(chat_history=thread_history)
                break

    def create_new_thread():
        new_thread_id = (
            max(int(thread.thread_id) for thread in st.session_state["threads"]) + 1
            if st.session_state["threads"]
            else 1
        )
        thread = chat.create_thread(f"Chat: {new_thread_id + 1}", username)
        st.session_state["threads"].insert(0, thread)
        select_thread(new_thread_id)

    st.sidebar.title("Chatter -> Chat")
    with st.sidebar.container(height=1000):
        st.button("+ New Chat", on_click=create_new_thread)
        # Sidebar UI for thread management

        st.header("Recent chats")
        for thread in st.session_state["threads"]:
            if st.button(thread.title, key=thread.thread_id):
                select_thread(thread.thread_id)

    if st.sidebar.button("Logout"):
        st.session_state["username"] = None
        set_cookie("username", "", 0)
        time.sleep(5)
        st.rerun()

    if st.sidebar.button("Agents"):
        st.session_state["current_page"] = "agents"
        st.rerun()

    # Main chat UI
    if st.session_state["current_thread_id"] is not None:
        current_thread = chat.get_thread(st.session_state["current_thread_id"])
        if current_thread:
            st.title(current_thread.title)
            # chat_agent = current_thread.agent

            with st.container(height=1000):
                # Display thread chat history
                messages = chat.read_messages(current_thread.thread_id)
                for message in messages:
                    with st.chat_message(
                        message.author.username, avatar=message.author.avatar
                    ):
                        st.markdown(message.content)

                placeholder = st.empty()

            with st.container():
                col1, col2 = st.columns([1, 9])

                # Place a dropdown in the first column
                with col1:
                    agents = chat.get_agent_names()
                    selected_agent = st.selectbox(
                        "Choose an agent:",
                        agents,
                        key="dropdown",
                        label_visibility="collapsed",
                        help="Choose an agent to chat with.",
                    )
                    # print(selected_agent)

                # Place a text input in the second column
                with col2:
                    user_input = st.chat_input(
                        "Type your message here:", key="msg_input"
                    )
                chat_agent = chat.get_agent(selected_agent)
                chat_agent.chat_history = messages
                chat_avatar = chat.get_participant(selected_agent).avatar

                if user_input:
                    with placeholder.container():
                        with st.chat_message(username, avatar=user.avatar):
                            st.markdown(user_input)
                            chat.post_message(
                                current_thread.thread_id, username, "user", user_input
                            )

                        with st.chat_message(chat_agent.name, avatar=chat_avatar):
                            st.write_stream(
                                chat_agent.get_response_stream(
                                    user_input, current_thread.id
                                )
                            )
                            chat.post_message(
                                current_thread.thread_id,
                                chat_agent.name,
                                "agent",
                                chat_agent.last_message,
                            )

                    st.rerun()
