import streamlit as st
from sqlalchemy import create_engine, text

def get_engine():
    db = st.secrets["db"]

    engine = create_engine(
        f"mysql+mysqlconnector://{db['user']}:{db['password']}@"
        f"{db['host']}:{db['port']}/{db['database']}",
        pool_pre_ping=True,
        connect_args={
            "connection_timeout": 5,   # seconds
        },
    )

    return engine
