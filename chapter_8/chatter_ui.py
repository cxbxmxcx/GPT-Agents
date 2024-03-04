import streamlit as st

from interface.agent import agent_page
from interface.chat import chat_page
from interface.login import login_page


def main():
    if username := st.session_state.get("username"):
        if current_page := st.session_state.get("current_page"):
            if current_page == "agents":
                # Placeholder for agents page
                agent_page(username)
                return
        chat_page(username)

    else:
        login_page()


if __name__ == "__main__":
    main()
