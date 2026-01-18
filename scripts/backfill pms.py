from database.db import SessionLocal
from database.models import Match, PlayerMatchStats

def backfill_match_dates():
    db = SessionLocal()

    print("Backfilling match_date in PlayerMatchStats...")

    pms_rows = db.query(PlayerMatchStats).all()
    updated = 0

    for pms in pms_rows:
        match = db.query(Match).filter(Match.id == pms.match_id).first()
        if match and match.date:
            pms.match_date = match.date
            updated += 1

    db.commit()
    db.close()

    print(f"Backfilled {updated} rows.")

if __name__ == "__main__":
    backfill_match_dates()
