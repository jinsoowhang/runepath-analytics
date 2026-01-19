import streamlit as st
from src.queries import top_spenders
from src.charts import bar_chart

st.title("Top Spenders")

# Toggle
metric_type = st.radio(
    "View values as:",
    options=["Gold", "Dollars"],
    horizontal=True
)

limit = st.slider("Number of players", 5, 50, 20)

df = top_spenders(limit)

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
    bar_chart(
        df,
        x="player",
        y=y_col,
        title=f"Top Players by {y_label}"
    ),
    use_container_width=True
)

# Table formatting
display_df = df.copy()
display_df[y_col] = display_df[y_col].round(2)

st.dataframe(display_df)

st.caption("Dollar values are estimates based on 50 gold = $1.")
