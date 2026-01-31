import streamlit as st
from src.queries import churned_players, total_unique_players

st.title("Churn Analysis")

# Slider for days inactive threshold
days_threshold = st.slider(
    "Days inactive threshold:",
    min_value=7,
    max_value=90,
    value=30,
    step=1
)

# Get churned players
df = churned_players(days_inactive=days_threshold)
total_players_df = total_unique_players()
total_players = total_players_df["total_players"].iloc[0] if not total_players_df.empty else 0

# Calculate metrics
churned_count = len(df)
churn_rate = (churned_count / total_players * 100) if total_players > 0 else 0

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Churned Players", f"{churned_count:,}")
col2.metric("Total Players", f"{int(total_players):,}")
col3.metric("Churn Rate", f"{churn_rate:.1f}%")

st.caption(f"Players who haven't logged in for more than {days_threshold} days")

# Table of churned players
if not df.empty:
    st.subheader("Churned Players")
    display_df = df.copy()
    display_df.columns = ["Player ID", "Player Name", "Last Login", "Days Inactive"]
    st.dataframe(display_df)
else:
    st.success(f"No players have been inactive for more than {days_threshold} days.")
