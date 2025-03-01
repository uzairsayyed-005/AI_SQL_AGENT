from langchain.sql_database import SQLDatabase
import streamlit as st

def get_db_uri(uploaded_file):
    if uploaded_file:
        with open("temp.db", "wb") as f:
            f.write(uploaded_file.getbuffer())
        return "sqlite:///temp.db"
    return "sqlite:///Chinook.db"

def display_schema_explorer(db_uri):
    with st.expander(" Database Schema Explorer", expanded=False):
        try:
            db = SQLDatabase.from_uri(db_uri)
            tables = db.get_usable_table_names()
            if tables:
                selected_table = st.selectbox("Select a table to view schema", tables)
                if selected_table:
                    table_info = db.get_table_info([selected_table])
                    st.markdown(f"### {selected_table} Schema")
                    st.code(table_info)
            else:
                st.warning("No tables found in the database")
        except Exception as e:
            st.error(f" Database connection error: {str(e)}")