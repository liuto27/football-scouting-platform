from database.db import SessionLocal
from database.models import League, Team, Player, Match, PlayerMatchStats
from scraper.transfermarkt.teams import scrape_teams_from_league
from scraper.transfermarkt.players import scrape_players_from_team
from scraper.transfermarkt.player_match_stats import scrape_player_match_stats
from scraper.transfermarkt.match_details import scrape_match_details


def get_or_create_team(db, id):
    team = db.query(Team).filter(Team.id == id).first()
    return team.id if team else None


def get_or_create_match(db, match_info, league_id):

    existing = db.query(Match).filter(Match.match_url == match_info["match_url"]).first()
    if existing:
        return existing.id

    match = Match(
        id=match_info["id"],
        date=match_info["date"],
        league_id=league_id,
        home_team_id=get_or_create_team(db, match_info["home_team_id"]),
        away_team_id=get_or_create_team(db, match_info["away_team_id"]),
        home_team_name=match_info["home_team_name"],
        away_team_name=match_info["away_team_name"],
        home_goals=match_info["home_goals"],
        away_goals=match_info["away_goals"],
        match_url=match_info["match_url"]
    )
    db.add(match)
    db.commit()
    return match.id


def populate_database():
    db = SessionLocal()

    print("=== Populating database ===")

    # 1. Insert Serie B manually
    league = db.query(League).filter(League.name == "Serie B").first()
    if not league:
        league = League(
            id="IT2",
            name="Serie B",
            country="Italy",
            league_url="https://www.transfermarkt.com/serie-b/startseite/wettbewerb/IT2"
        )
        db.add(league)
        db.commit()
        print("Inserted Serie B")

    # 2. Scrape teams
    print("\nScraping teams...")
    teams = scrape_teams_from_league(league.league_url)

    # DELETE!!!!------------------------------------------------------------------------------------------------------------------------
    teams = teams[:3]  # sample: first X teams
    # -----------------------------------------------------------------------------------------------------------------------------

    inserted_teams = 0
    for t in teams:
        existing = db.query(Team).filter(Team.name == t["name"]).first()
        if not existing:
            team = Team(
                id=t["id"],
                name=t["name"],
                team_url=t["url"],
                league_id=league.id
            )
            db.add(team)
            inserted_teams += 1
    db.commit()
    print(f"Inserted {inserted_teams} teams")


    # 3. Scrape players
    print("\nScraping players...")
    all_players = []
    inserted_players = 0
    for team in db.query(Team).all():
        players = scrape_players_from_team(team.team_url)

        # DELETE!!!!------------------------------------------------------------------------------------------------------------------------
        players = players[:3]  # sample: first X players
        # -----------------------------------------------------------------------------------------------------------------------------------------

        for p in players:
            existing = db.query(Player).filter(Player.name == p["name"]).first()
            if not existing:
                player = Player(
                    id=p["id"],
                    name=p["name"],
                    player_url=p["player_url"],
                    birthdate=p["birthdate"],
                    nationality=p["nationality"],
                    position=p["position"]
                )
                db.add(player)
                inserted_players += 1
                all_players.append(player)
    db.commit()
    print(f"Inserted {inserted_players} players")


    # 4. Scrape player match stats and collect match URLs
    print("\nScraping player match stats...")
    match_urls = set()

    for player in db.query(Player).all():
        inserted_matches_per_player = 0
        stats = scrape_player_match_stats(player.player_url)
        print(f"Searching for matches played by {player.id} ({player.name})...")
        for s in stats:
            match_urls.add(s["match_url"])
            existing = db.query(PlayerMatchStats).filter_by(
                player_id=player.id,
                match_id=s["match_id"]
            ).first()

            if existing:
                continue  # or update fields if you want

            pms = PlayerMatchStats(
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
            db.add(pms)
            inserted_matches_per_player += 1
        print(f"Collected {inserted_matches_per_player} unique matches for player {player.id}")
    db.commit()

    # 5. Scrape match details and insert matches
    print("\nScraping match details...")
    for url in match_urls:
        match_info = scrape_match_details(url)
        get_or_create_match(db, match_info, league.id)

    print("\n=== Database population complete ===")
    db.close()


if __name__ == "__main__":
    populate_database()
