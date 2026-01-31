import pandas as pd
import streamlit as st
from datetime import date
from src.db import get_engine

engine = get_engine()

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


# ========== Player Retention Queries ==========


@st.cache_data(ttl=300)  # Cache for 5 minutes
def daily_active_users():
    query = """
    SELECT 
        DATE(login_time) AS day,
        COUNT(DISTINCT a.id) AS active_players
    FROM player_logins pl
    JOIN players p 
      ON pl.player_id = p.id
    JOIN accounts a
      ON p.account_id = a.id
    WHERE a.id NOT IN (13)  -- Exclude God Account
    GROUP BY day
    ORDER BY day;
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=300)
def monthly_active_users():
    query = """
    SELECT
        DATE_FORMAT(login_time, '%Y-%m') AS month,
        COUNT(DISTINCT a.id) AS active_players
    FROM player_logins pl
    JOIN players p 
      ON pl.player_id = p.id
    JOIN accounts a
      ON p.account_id = a.id
    WHERE a.id NOT IN (13)  -- Exclude God Account
    GROUP BY month
    ORDER BY month;
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=300)
def new_vs_returning_daily():
    query = """
    WITH first_logins AS (
        SELECT
            player_id,
            DATE(MIN(login_time)) AS first_login_date
        FROM player_logins
        WHERE player_id NOT IN (19, 29)
        GROUP BY player_id
    ),
    daily_logins AS (
        SELECT
            DATE(login_time) AS day,
            player_id
        FROM player_logins
        WHERE player_id NOT IN (19, 29)
        GROUP BY day, player_id
    )
    SELECT
        dl.day,
        SUM(CASE WHEN dl.day = fl.first_login_date THEN 1 ELSE 0 END) AS new_players,
        SUM(CASE WHEN dl.day > fl.first_login_date THEN 1 ELSE 0 END) AS returning_players
    FROM daily_logins dl
    JOIN first_logins fl ON dl.player_id = fl.player_id
    GROUP BY dl.day
    ORDER BY dl.day;
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=300)
def cohort_retention():
    query = """
    WITH first_logins AS (
        SELECT
            player_id,
            DATE_FORMAT(MIN(login_time), '%Y-%m') AS cohort_month
        FROM player_logins
        WHERE player_id NOT IN (19, 29)
        GROUP BY player_id
    ),
    monthly_activity AS (
        SELECT
            player_id,
            DATE_FORMAT(login_time, '%Y-%m') AS activity_month
        FROM player_logins
        WHERE player_id NOT IN (19, 29)
        GROUP BY player_id, activity_month
    )
    SELECT
        fl.cohort_month,
        ma.activity_month,
        COUNT(DISTINCT ma.player_id) AS active_players,
        (SELECT COUNT(DISTINCT player_id) FROM first_logins WHERE cohort_month = fl.cohort_month) AS cohort_size,
        PERIOD_DIFF(REPLACE(ma.activity_month, '-', ''), REPLACE(fl.cohort_month, '-', '')) AS months_since_join
    FROM first_logins fl
    JOIN monthly_activity ma ON fl.player_id = ma.player_id
    GROUP BY fl.cohort_month, ma.activity_month
    ORDER BY fl.cohort_month, ma.activity_month;
    """
    return pd.read_sql(query, engine)


def churned_players(days_inactive=30):
    query = f"""
    WITH last_logins AS (
        SELECT
            player_id,
            MAX(login_time) AS last_login
        FROM player_logins
        WHERE player_id NOT IN (19, 29)
        GROUP BY player_id
    ),
    player_names AS (
        SELECT id, name FROM players
    )
    SELECT
        ll.player_id,
        pn.name AS player_name,
        ll.last_login,
        DATEDIFF(NOW(), ll.last_login) AS days_inactive
    FROM last_logins ll
    LEFT JOIN player_names pn ON ll.player_id = pn.id
    WHERE DATEDIFF(NOW(), ll.last_login) > {days_inactive}
    ORDER BY ll.last_login DESC;
    """
    return pd.read_sql(query, engine)


def total_unique_players():
    query = """
    SELECT COUNT(DISTINCT player_id) AS total_players
    FROM player_logins
    WHERE player_id NOT IN (19, 29);
    """
    return pd.read_sql(query, engine)
