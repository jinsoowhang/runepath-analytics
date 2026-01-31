import streamlit as st

st.title("Player Retention")

st.write("""
This section tracks player engagement and retention metrics.

Use the subpages to explore:
- **Active Users** - Daily and monthly active user trends
- **Cohort Analysis** - Retention rates by signup cohort
- **Churn** - Identify inactive players
""")

st.info("Players 19 and 29 are excluded from all metrics (test accounts).")
