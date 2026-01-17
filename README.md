Serie B Scouting Platform – MVP
A lightweight, production‑ready scouting engine built on real match data from Serie B.
Designed for scouts who want fast insights, young talent discovery, and simple, powerful queries.

🚀 What this MVP does
This MVP scrapes and stores:

Teams in Serie B

Players (name, birthdate, nationality, position)

Matches (date, teams, goals)

PlayerMatchStats (minutes, goals, assists, cards)

All data is stored in a clean SQLite database with a normalized schema.

A Streamlit dashboard lets scouts explore:

Young debutants

High‑usage U21 players

Players who scored on debut

Players with rising minutes

Team-by-team youth usage

🧠 Why this MVP is valuable for scouts
Scouts often miss:

young players who quietly debut

players who get their first real minutes

players who switch teams and immediately perform

players who accumulate meaningful minutes without hype

This MVP surfaces exactly those profiles.

Example scouting questions you can answer:
“Show me all players under 19 who debuted in Serie B last week.”

“Which players scored in their first match this season?”

“Which U21 players have played more than 300 minutes so far?”

“Which young forwards have at least 3 goals in the last 5 matches?”

“Which teams rely most on U21 players?”

All of these are supported by the current schema.


📦 1. Initial full scrape
bash
python scripts/reset_database.py
python scripts/create_tables.py
python scripts/populate_database.py
This loads the entire Serie B season into the database.

🔄 2. Weekly incremental updates
Run:

bash
python scripts/update_database.py
This will:

detect new matches since last update

scrape only those matches

insert only new PlayerMatchStats

avoid re-scraping old data

keep the DB always up to date

Perfect for a weekly scheduler.

📊 3. Streamlit dashboard
Run locally:

bash
streamlit run app.py
Deploy on Streamlit Cloud:

Push repo to GitHub

Connect to Streamlit Cloud

Select app.py as entrypoint

(Optional) Add a weekly scheduled job to run update_database.py

🗺️ 4. Roadmap to a top‑tier scouting platform
Phase 1 — MVP (done)
Serie B data

Young player discovery

Debut detection

Streamlit dashboard

Phase 2 — Better data
Add more leagues

Add more stats (shots, passes, duels)

Add player profile pages

Phase 3 — Diretta integration
Ratings

Advanced match stats

Player performance trends

Phase 4 — Product features
User accounts

Saved filters

Watchlists

Notes per player

CSV/Excel export

Phase 5 — Intelligence layer
Natural language queries

Player similarity models

Breakout potential predictions

Alerts (“New U19 debutant this weekend”)

Phase 6 — Commercial platform
Multi-league coverage

API access

Club dashboards

Scouting reports generation

❤️ Why this project matters
Football scouting is still dominated by:

intuition

word of mouth

incomplete data

slow tools

This MVP is the first step toward a fast, modern, data‑driven scouting engine that helps scouts discover talent before anyone else.
