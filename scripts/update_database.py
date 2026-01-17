from datetime import date, timedelta
from database.db import SessionLocal
from database.models import Match, Team, Player, PlayerMatchStats
from scraper.transfermarkt.teams import scrape_teams_from_league
from scraper.transfermarkt.players import scrape_players_from_team
from scraper.transfermarkt.player_match_stats import scrape_player_match_stats
from scraper.transfermarkt.match_details import scrape_match_details


def get_latest_match_date(db):
    latest = db.query(Match).order_by(Match.date.desc()).first()
    return latest.date if latest else date(2000, 1, 1)


def update_database():
    db = SessionLocal()
    print("=== Incremental Update Started ===")

    latest_date = get_latest_match_date(db)
    print(f"Last match in DB: {latest_date}")

    # 1. Get all teams in Serie B
    teams = db.query(Team).all()

    new_matches = 0
    new_stats = 0

    for team in teams:
        print(f"\nChecking new matches for {team.name}...")
        matches = scrape_players_from_team(team.team_url)  # returns players, not matches
        # Correction: we need a match list scraper
        # For MVP, use player stats to discover new matches

        # 2. For each player in this team, scrape match stats
        players = (
            db.query(Player)
            .join(PlayerMatchStats, Player.id == PlayerMatchStats.player_id)
            .filter(PlayerMatchStats.team_id == team.id)
            .distinct()
            .all()
        )

        for player in players:
            stats = scrape_player_match_stats(player.player_url)

            for s in stats:
                match_date = s["date"]
                if match_date <= latest_date:
                    continue  # old match, skip

                # Insert match if new
                existing_match = (
                    db.query(Match)
                    .filter(Match.match_url == s["match_url"])
                    .first()
                )

                if not existing_match:
                    match_info = scrape_match_details(s["match_url"])
                    match = Match(
                        id=match_info["match_id"],
                        date=match_info["date"],
                        league_id=team.league_id,
                        home_team_id=match_info["home_team_id"],
                        away_team_id=match_info["away_team_id"],
                        home_team_name=match_info["home_team"],
                        away_team_name=match_info["away_team"],
                        home_goals=match_info["home_goals"],
                        away_goals=match_info["away_goals"],
                        match_url=match_info["match_url"]
                    )
                    db.add(match)
                    db.commit()
                    new_matches += 1
                    print(f"Added new match: {match_info['match_url']}")

                # Insert player stats if new
                pms = (
                    db.query(PlayerMatchStats)
                    .filter(
                        PlayerMatchStats.player_id == player.id,
                        PlayerMatchStats.match_id == s["match_id"]
                    )
                    .first()
                )

                if not pms:
                    new_pms = PlayerMatchStats(
                        player_id=player.id,
                        match_id=s["match_id"],
                        team_id=s["team_id"],
                        minutes=s["minutes"],
                        goals=s["goals"],
                        assists=s["assists"],
                        yellow=s["yellow"],
                        second_yellow=s["second_yellow"],
                        red=s["red"]
                    )
                    db.add(new_pms)
                    new_stats += 1

        db.commit()

    print("\n=== Incremental Update Complete ===")
    print(f"New matches added: {new_matches}")
    print(f"New player stats added: {new_stats}")

    db.close()


if __name__ == "__main__":
    update_database()
