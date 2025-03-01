import streamlit as st
from callbacks import IntermediateStepHandler
from database import get_db_uri, display_schema_explorer
from agent_setup import init_agent
from chat_history import init_chat_history, display_chat_history
from langchain.callbacks.streamlit import StreamlitCallbackHandler

# Initialize app
st.set_page_config(page_title="SQL Database Chat Agent", page_icon="", layout="wide")
st.title(" Smart Database Assistant")

# Initialize chat history
init_chat_history()

# Sidebar configuration
with st.sidebar:
    st.header(" Settings")
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Required for LLM access - get from https://console.groq.com",
        key="groq_api_key"
    )
    uploaded_file = st.file_uploader(
        "Upload SQLite Database", 
        type=["db", "sqlite"],
        help="Use default Chinook DB if not provided"
    )

# Database setup
db_uri = get_db_uri(uploaded_file)
display_schema_explorer(db_uri)

# Display chat history
display_chat_history()

# Process user input
if prompt := st.chat_input("Ask your database question..."):
    # Validate API key
    if not st.session_state.groq_api_key:
        st.error("❌ API key required - enter your Groq API key in the sidebar")
        st.stop()
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Initialize agent
    agent = init_agent(db_uri, st.session_state.groq_api_key)
    if not agent:
        st.stop()

    # Process query
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        step_handler = IntermediateStepHandler()
        
        try:
            response = agent.run(
                {
                    "input": f"""Answer the question step by step. Follow these rules:
                    1. Use only plain text format
                    2. Never use markdown or special formatting
                    3. If you need to show SQL, wrap it in triple backticks
                    4. Be concise but thorough
                    5. If unsure, ask for clarification
                    Question: {prompt}"""
                },
                callbacks=[st_callback, step_handler]
            )
            
            # Format the response
            formatted_response = f"**Answer**\n\n{response}"
            st.markdown(formatted_response)
            
            # Save to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": formatted_response,
                "intermediate_steps": step_handler.steps
            })
        except Exception as e:
            # Handle errors gracefully
            error_msg = f"""**Error Processing Query**\n
            The query could not be processed. Please try rephrasing your question or check the database connection.\n
            **Technical Details:**\n
            ```{str(e)}```"""
            st.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })