from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from langchain.sql_database import SQLDatabase
import streamlit as st

def init_agent(db_uri, api_key):
    try:
        if not api_key:
            raise ValueError("Groq API key is required")
            
        db = SQLDatabase.from_uri(db_uri)
        llm = ChatGroq(
            model_name="llama3-8b-8192", 
            groq_api_key=api_key,
            temperature=0  # Added for more deterministic output
        )
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        
        return create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type="zero-shot-react-description",
            handle_parsing_errors="Check your output and make sure it conforms! If unsure, ask the user for clarification.",  # Updated handling
            max_iterations=10  
        )
    except Exception as e:
        st.error(f" Agent initialization failed: {str(e)}")
        return None