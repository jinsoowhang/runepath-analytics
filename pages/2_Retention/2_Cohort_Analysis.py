import streamlit as st
import pandas as pd
from src.queries import cohort_retention
from src.charts import heatmap

st.title("Cohort Retention Analysis")

df = cohort_retention()

if not df.empty:
    # Create pivot table for heatmap
    # Calculate retention percentage
    df["retention_pct"] = (df["active_players"] / df["cohort_size"] * 100).round(1)

    # Pivot for heatmap: cohort_month as rows, months_since_join as columns
    pivot_df = df.pivot_table(
        index="cohort_month",
        columns="months_since_join",
        values="retention_pct",
        aggfunc="first"
    )

    # Rename columns to be more readable
    pivot_df.columns = [f"Month {int(c)}" for c in pivot_df.columns]

    st.subheader("Retention by Cohort (%)")

    # Create heatmap
    fig = heatmap(
        z=pivot_df.values,
        x=list(pivot_df.columns),
        y=list(pivot_df.index),
        z_label="Retention %",  # ✅ Use z_label instead
        title="Cohort Retention Heatmap",
        color_scale="Blues"
    )
    fig.update_layout(
        xaxis_title="Months Since Join",
        yaxis_title="Cohort (Join Month)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Each row represents players who first logged in during that month. Values show % still active in subsequent months.")

    # Show raw data
    st.subheader("Cohort Data")
    display_df = df[["cohort_month", "months_since_join", "active_players", "cohort_size", "retention_pct"]].copy()
    display_df.columns = ["Cohort", "Months Since Join", "Active Players", "Cohort Size", "Retention %"]
    st.dataframe(display_df)

else:
    st.warning("No cohort data available.")
