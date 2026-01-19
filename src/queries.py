import pandas as pd
from src.db import get_engine

engine = get_engine()

def daily_gold_spent():
    query = """
    SELECT 
        DATE(date) AS day,
        SUM(cost) AS total_gold_spent,
        SUM(cost)/50 AS estimated_dollar_spend
    FROM shop_history
    WHERE cost > 0
    GROUP BY day
    ORDER BY day;
    """
    return pd.read_sql(query, engine)

def top_shop_items(limit=20):
    query = f"""
    SELECT 
        title,
        COUNT(*) AS purchases,
        SUM(cost) AS total_gold_spent,
        SUM(cost)/50 AS estimated_dollar_spend
    FROM shop_history
    WHERE cost > 0
    GROUP BY title
    ORDER BY total_gold_spent DESC
    LIMIT {limit};
    """
    return pd.read_sql(query, engine)

def top_spenders(limit=20):
    query = f"""
    SELECT 
        player,
        SUM(cost) AS total_gold_spent,
        SUM(cost)/50 AS estimated_dollar_spend
    FROM shop_history
    WHERE cost > 0
    GROUP BY player
    ORDER BY total_gold_spent DESC
    LIMIT {limit};
    """
    return pd.read_sql(query, engine)

def monthly_gold_spent():
    query = """
    SELECT 
        DATE_FORMAT(date, '%Y-%m') AS month,
        SUM(cost) AS total_gold_spent,
        SUM(cost)/50 AS estimated_dollar_spend
    FROM shop_history
    WHERE cost > 0
    GROUP BY month
    ORDER BY month;
    """
    return pd.read_sql(query, engine)
