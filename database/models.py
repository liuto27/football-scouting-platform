from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, Float, Boolean, PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship
from .db import Base


class League(Base):
    __tablename__ = "leagues"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    league_url = Column(String, nullable=True)

    teams = relationship("Team", back_populates="league")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    league_url = Column(String, nullable=True)
    team_url = Column(String, nullable=True)
    league_id = Column(Integer, ForeignKey("leagues.id"))

    league = relationship("League", back_populates="teams")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    player_url = Column(String, nullable=True)
    birthdate = Column(Date)
    nationality = Column(String)
    position = Column(String)

    match_stats = relationship("PlayerMatchStats", back_populates="player")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"))

    # Foreign keys
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))

    # Denormalized names (no FK)
    home_team_name = Column(String, nullable=False)
    away_team_name = Column(String, nullable=False)

    home_goals = Column(Integer)
    away_goals = Column(Integer)
    match_url = Column(String, unique=True)
    diretta_url = Column(String, nullable=True)  # <-- NEW

    league = relationship("League")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])

    player_stats = relationship("PlayerMatchStats", back_populates="match")


class PlayerMatchStats(Base):
    __tablename__ = "player_match_stats"

    player_id = Column(Integer, ForeignKey("players.id"))
    match_id = Column(Integer, ForeignKey("matches.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    match_date = Column(Date)

    minutes = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    yellow = Column(Boolean)
    second_yellow = Column(Boolean)
    red = Column(Boolean)
    rating = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint("player_id", "match_id"),
    )

    player = relationship("Player", back_populates="match_stats")
    match = relationship("Match", back_populates="player_stats")

