import streamlit as st
from src.queries import daily_active_users, monthly_active_users
from src.charts import line_chart

st.title("Active Users")

# Toggle between DAU and MAU
view_type = st.radio(
    "View:",
    options=["Daily (DAU)", "Monthly (MAU)"],
    horizontal=True
)

if view_type == "Daily (DAU)":
    df = daily_active_users()
    x_col = "day"
    y_col = "active_players"
    title = "Daily Active Users"

    if not df.empty:
        # KPIs
        current_dau = df[y_col].iloc[-1] if len(df) > 0 else 0
        avg_7d = df[y_col].tail(7).mean() if len(df) >= 7 else df[y_col].mean()
        avg_30d = df[y_col].tail(30).mean() if len(df) >= 30 else df[y_col].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("Current DAU", f"{int(current_dau):,}")
        col2.metric("7-Day Avg", f"{avg_7d:,.1f}")
        col3.metric("30-Day Avg", f"{avg_30d:,.1f}")

        # Chart
        st.plotly_chart(
            line_chart(df, x=x_col, y=y_col, title=title),
            use_container_width=True
        )

        # Table
        st.dataframe(df)
    else:
        st.warning("No login data available.")

else:
    df = monthly_active_users()
    x_col = "month"
    y_col = "active_players"
    title = "Monthly Active Users"

    if not df.empty:
        # KPIs
        current_mau = df[y_col].iloc[-1] if len(df) > 0 else 0
        avg_mau = df[y_col].mean()

        col1, col2 = st.columns(2)
        col1.metric("Current MAU", f"{int(current_mau):,}")
        col2.metric("Average MAU", f"{avg_mau:,.1f}")

        # Chart
        st.plotly_chart(
            line_chart(df, x=x_col, y=y_col, title=title),
            use_container_width=True
        )

        # Table
        st.dataframe(df)
    else:
        st.warning("No login data available.")
