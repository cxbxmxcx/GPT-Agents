import time

import streamlit as st
from streamlit_js_eval import set_cookie

from chatter.chat_system import ChatSystem


def get_cookie(name, default=None):
    """
    WARNING: This uses unsupported feature of Streamlit
    Returns the cookies as a dictionary of kv pairs
    It is nesscary as the streamlit_js_eval get_cookie causes undesired behavior
    """
    # https://github.com/streamlit/streamlit/pull/5457
    from urllib.parse import unquote

    from streamlit.web.server.websocket_headers import _get_websocket_headers

    headers = _get_websocket_headers()
    if headers is None:
        return {}

    if "Cookie" not in headers:
        return {}

    cookie_string = headers["Cookie"]
    # A sample cookie string: "K1=V1; K2=V2; K3=V3"
    cookie_kv_pairs = cookie_string.split(";")

    cookie_dict = {}
    for kv in cookie_kv_pairs:
        k_and_v = kv.split("=")
        k = k_and_v[0].strip()
        v = k_and_v[1].strip()
        cookie_dict[k] = unquote(
            v
        )  # e.g. Convert name%40company.com to name@company.com

    return cookie_dict.get(name)


emoji_faces = [
    "😀",
    "😃",
    "😄",
    "😁",
    "😆",
    "😅",
    "🤣",
    "😂",
    "🙂",
    "🙃",
    "😉",
    "😊",
    "😇",
    "🥰",
    "😍",
    "😘",
    "😗",
    "😙",
    "😚",
    "😋",
    "😛",
    "😜",
    "🤪",
    "😝",
    "🤑",
]


def login_page():
    if username := get_cookie("username", "username"):
        st.session_state["username"] = username
        st.rerun()

    chat = ChatSystem()

    st.title("Login or Create New User")

    menu = ["Login", "Create New User"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login Section")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if chat.login(username, password):
                st.success(f"Welcome {username}")
                set_cookie("username", username, 30)
                time.sleep(
                    1
                )  # This is a hack to make sure the cookie is set before the page reruns
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Incorrect Username/Password")

    elif choice == "Create New User":
        st.subheader("Create New Account")
        new_username = st.text_input("Username")
        avatar = st.selectbox("Choose an avatar", emoji_faces)
        new_password = st.text_input("Password", type="password")

        if st.button("Create User"):
            if chat.add_participant(
                new_username, new_password, new_username, avatar=avatar
            ):
                threads = chat.get_all_threads()
                for thread in threads:
                    chat.subscribe_to_thread(thread.thread_id, new_username)
                st.success(f"User {new_username} created successfully.")
                st.session_state["username"] = new_username
                st.rerun()
            else:
                st.error("User already exists. Please choose a different username.")
