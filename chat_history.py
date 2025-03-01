import streamlit as st

def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Welcome!  Upload a SQLite database and enter your Groq API key to start!"
        }]

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "intermediate_steps" in message and message["intermediate_steps"]:
                with st.expander("View Reasoning Process"):
                    st.markdown("\n\n".join(message["intermediate_steps"]))