import streamlit as st
from src.queries import daily_gold_spent
from src.charts import line_chart
from src.db import get_engine

st.title("Overview")

df = daily_gold_spent()

# Toggle
metric_type = st.radio(
    "View values as:",
    options=["Gold", "Dollars"],
    horizontal=True
)

if metric_type == "Gold":
    y_col = "total_gold_spent"
    y_label = "Total Gold Spent"
    value_formatter = lambda x: f"{int(x):,}"
else:
    y_col = "estimated_dollar_spend"
    y_label = "Estimated Dollar Spend"
    value_formatter = lambda x: f"${x:,.2f}"

# KPIs
total_value = df[y_col].sum()
latest_day = df["day"].max()

col1, col2 = st.columns(2)
col1.metric(y_label, value_formatter(total_value))
col2.metric("Last Recorded Day", str(latest_day))

# Chart
st.plotly_chart(
    line_chart(
        df,
        x="day",
        y=y_col,
        title=f"Daily {y_label}"
    ),
    use_container_width=True
)

# Table (rename columns for clarity)
display_df = df.copy()
display_df[y_col] = display_df[y_col].round(2)

st.dataframe(display_df)
