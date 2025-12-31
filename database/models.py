from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, Float, Boolean
)
from sqlalchemy.orm import relationship
from .db import Base


class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    teams = relationship("Team", back_populates="league")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"))

    league = relationship("League", back_populates="teams")
    players_history = relationship("PlayerTeamHistory", back_populates="team")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birthdate = Column(Date)
    nationality = Column(String)
    position = Column(String)

    match_stats = relationship("PlayerMatchStats", back_populates="player")
    team_history = relationship("PlayerTeamHistory", back_populates="player")


class PlayerTeamHistory(Base):
    __tablename__ = "player_team_history"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)

    player = relationship("Player", back_populates="team_history")
    team = relationship("Team", back_populates="players_history")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"))
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    home_goals = Column(Integer)
    away_goals = Column(Integer)
    match_url = Column(String)

    league = relationship("League")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
    player_stats = relationship("PlayerMatchStats", back_populates="match")


class PlayerMatchStats(Base):
    __tablename__ = "player_match_stats"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    match_id = Column(Integer, ForeignKey("matches.id"))

    minutes_played = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    yellow_cards = Column(Integer)
    red_cards = Column(Integer)
    rating = Column(Float)
    starter = Column(Boolean)
    substitution_in_minute = Column(Integer)
    substitution_out_minute = Column(Integer)

    player = relationship("Player", back_populates="match_stats")
    match = relationship("Match", back_populates="player_stats")
