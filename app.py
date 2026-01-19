import streamlit as st

st.set_page_config(
    page_title="RunePath Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("RunePath Analytics")

pages = {
    "Home": [
        st.Page("pages/0_Home.py", title="Overview"),
    ],
    "Spend Tracker": [
        st.Page("pages/1_Spend_Tracker/0_Spend_Tracker.py", title="Overview"),
        st.Page("pages/1_Spend_Tracker/1_Overview.py", title="Daily Spend"),
        st.Page("pages/1_Spend_Tracker/2_Top_Items.py", title="Top Items"),
        st.Page("pages/1_Spend_Tracker/3_Top_Players.py", title="Top Players"),
        st.Page("pages/1_Spend_Tracker/4_Monthly_Trends.py", title="Monthly Trends"),
    ],
}

pg = st.navigation(pages)
pg.run()
