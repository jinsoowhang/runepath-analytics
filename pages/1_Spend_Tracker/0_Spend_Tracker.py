import streamlit as st

st.title("Spend Tracker")

st.write("""
This section tracks how gold leaves the economy through the shop.

Use the subpages to explore:
- Overall spending trends
- Top gold sinks
- Top spenders
- Monthly patterns

Note: God and GM accounts are filtered out because they’re used for testing.
""")

st.info("Dollar values are estimated using a 50 gold = $1 conversion.")
