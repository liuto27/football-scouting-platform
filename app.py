import streamlit as st
from database.db import SessionLocal
from database.models import Player, Match, PlayerMatchStats, Team
from datetime import date, timedelta
from sqlalchemy import func

st.set_page_config(page_title="Serie B Scouting MVP", layout="wide")

@st.cache_resource
def get_db():
    return SessionLocal()

db = get_db()

st.title("Serie B Scouting – MVP")

st.sidebar.header("Filters")

# Age filter
max_age = st.sidebar.slider("Max age", 16, 25, 19)

# Date range for debut
days_back = st.sidebar.slider("Look back (days)", 1, 60, 7)
start_date = date.today() - timedelta(days=days_back)

st.subheader("Young debutants in Serie B")

# Example: debut in Serie B within last X days
subq = (
    db.query(
        PlayerMatchStats.player_id,
        func.min(Match.date).label("first_match_date")
    )
    .join(Match, Match.id == PlayerMatchStats.match_id)
    .group_by(PlayerMatchStats.player_id)
    .subquery()
)

q = (
    db.query(Player.name, Player.birthdate, subq.c.first_match_date)
    .join(subq, subq.c.player_id == Player.id)
    .filter(subq.c.first_match_date >= start_date)
)

# Age filter
today = date.today()
players = []
for name, birthdate, first_match_date in q.all():
    if birthdate:
        age = (today - birthdate).days // 365
        if age <= max_age:
            players.append({
                "name": name,
                "age": age,
                "first_match_date": first_match_date
            })

st.dataframe(players)
