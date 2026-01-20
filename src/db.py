import streamlit as st
from sqlalchemy import create_engine

def get_engine():
    db = st.secrets["db"]

    return create_engine(
        f"mysql+mysqlconnector://{db['user']}:{db['password']}@"
        f"{db['host']}:{db['port']}/{db['database']}"
    )
