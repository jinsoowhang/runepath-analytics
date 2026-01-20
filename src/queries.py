import pandas as pd
import streamlit as st
from datetime import date
from src.db import get_engine

def day_key():
    return date.today().isoformat()

@st.cache_data
def daily_gold_spent(_day_key):
    engine = get_engine()
    query = """
    SELECT 
        DATE(date) AS day,
        SUM(cost) AS total_gold_spent,
        SUM(cost)/50 AS estimated_dollar_spend
    FROM shop_history
    WHERE cost > 0
      AND player NOT IN (19, 29)
    GROUP BY day
    ORDER BY day;
    """
    return pd.read_sql(query, engine)

@st.cache_data
def top_shop_items(_day_key):
    engine = get_engine()
    query = f"""
    SELECT 
        title,
        COUNT(*) AS purchases,
        SUM(cost) AS total_gold_spent,
        SUM(cost)/50 AS estimated_dollar_spend
    FROM shop_history
    WHERE cost > 0
      AND player NOT IN (19, 29)
    GROUP BY title
    ORDER BY total_gold_spent DESC;
    """
    return pd.read_sql(query, engine)

@st.cache_data
def top_spenders(_day_key):
    engine = get_engine()
    query = f"""
    WITH player_cte as (

    SELECT 
        id,
        name
    FROM players

    )

    SELECT 
        s.player as player_id,
        p.name as player_name,
        SUM(cost) AS total_gold_spent,
        SUM(cost)/50 AS estimated_dollar_spend
    FROM player_cte p 
    JOIN shop_history s
    ON p.id = s.player 
    WHERE s.player NOT IN (19, 29)
    GROUP BY s.player, p.name
    ORDER BY total_gold_spent DESC;
    """
    return pd.read_sql(query, engine)

@st.cache_data
def monthly_gold_spent(_day_key):
    engine = get_engine()
    query = """
    SELECT 
        DATE_FORMAT(date, '%Y-%m') AS month,
        SUM(cost) AS total_gold_spent,
        SUM(cost)/50 AS estimated_dollar_spend
    FROM shop_history
    WHERE cost > 0
      AND player NOT IN (19, 29)
    GROUP BY month
    ORDER BY month;
    """
    return pd.read_sql(query, engine)
