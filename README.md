# RunePath Analytics

Analytics dashboard for the RunePath game server — tracks in-game economy and player engagement to help with game balancing and server health.

## Features

### Spend Tracker
- **Daily Spend Overview** — gold and USD equivalent trends over time (50 gold = $1)
- **Top Shop Items** — which items generate the most revenue, with purchase counts
- **Top Spenders** — player leaderboard ranked by total spend
- **Monthly Trends** — month-over-month spending patterns

### Player Retention
- **DAU / MAU** — daily and monthly active user counts with 7-day and 30-day rolling averages
- **Cohort Retention Heatmap** — what percentage of each signup cohort stays active month-over-month
- **Churn Analysis** — adjustable inactivity threshold to identify at-risk players

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Streamlit |
| Charts | Plotly |
| Data | pandas, SQLAlchemy |
| Database | MariaDB |
| Dev | Docker devcontainer, Python 3.11 |

## Architecture

```
MariaDB (game server)
  └── SQLAlchemy queries
        └── pandas DataFrames
              └── Plotly charts
                    └── Streamlit UI
```

## Project Structure

```
runepath-analytics/
├── app.py                    # Entry point
├── pages/
│   ├── 0_Home.py
│   ├── 1_Spend_Tracker/      # 4 spend analysis pages
│   └── 2_Retention/          # 4 retention analysis pages
└── src/
    ├── db.py                 # Database connection
    ├── queries.py            # SQL queries
    └── charts.py             # Reusable Plotly components
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Requires a `.streamlit/secrets.toml` with MariaDB credentials.
