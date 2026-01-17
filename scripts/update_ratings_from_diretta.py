from database.db import SessionLocal
from database.models import Match, PlayerMatchStats
from scraper.diretta.ratings import scrape_diretta_player_ratings
from utils.name_matching import find_player_in_match


def update_match_ratings_from_diretta(match_id: int):
    db = SessionLocal()

    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        print(f"Match {match_id} not found.")
        db.close()
        return

    if not match.diretta_url:
        print(f"No Diretta URL stored for match {match_id}.")
        db.close()
        return
    

    print(f"Scraping ratings for match {match_id}...")
    ratings = scrape_diretta_player_ratings(match.diretta_url)

    updated = 0
    unmatched = []

    for r in ratings:
        player = find_player_in_match(db, match_id, r["player_name"])

        if not player:
            unmatched.append(r["player_name"])
            continue

        pms = (
            db.query(PlayerMatchStats)
            .filter(
                PlayerMatchStats.player_id == player.id,
                PlayerMatchStats.match_id == match_id
            )
            .first()
        )

        if not pms:
            continue  # player exists but did not play (unused sub)

        pms.rating = r["rating"]
        updated += 1

    db.commit()
    db.close()

    print(f"Updated {updated} ratings for match {match_id}.")
    if unmatched:
        print("Unmatched players:", set(unmatched))


update_match_ratings_from_diretta(876)