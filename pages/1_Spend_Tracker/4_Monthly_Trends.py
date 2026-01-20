import streamlit as st
from src.queries import monthly_gold_spent, day_key
from src.charts import line_chart

st.title("Monthly Gold Trends")

# Toggle
metric_type = st.radio(
    "View values as:",
    options=["Dollars", "Gold"],
    horizontal=True
)

df = monthly_gold_spent(day_key())

if metric_type == "Gold":
    y_col = "total_gold_spent"
    y_label = "Total Gold Spent"
    value_formatter = lambda x: f"{int(x):,}"
else:
    y_col = "estimated_dollar_spend"
    y_label = "Estimated Dollar Spend"
    value_formatter = lambda x: f"${x:,.2f}"

# Chart
st.plotly_chart(
    line_chart(
        df,
        x="month",
        y=y_col,
        title=f"Monthly {y_label}"
    ),
    use_container_width=True
)

# Table formatting
display_df = df.copy()
display_df[y_col] = display_df[y_col].round(2)

st.dataframe(display_df)

st.caption("Dollar values are estimates based on 50 gold = $1.")
