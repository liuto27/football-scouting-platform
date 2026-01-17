import unicodedata
import re
from difflib import SequenceMatcher
from database.models import Player, PlayerMatchStats


def normalize_name(name: str) -> str:
    if not name:
        return ""
    name = name.lower().strip()
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def find_player_in_match(db, match_id: int, raw_name: str, threshold: float = 0.75):
    """
    Given a match_id and a raw Diretta player name,
    return the Player object that best matches.
    """
    norm_target = normalize_name(raw_name)
    if not norm_target:
        return None

    # Get all players who appear in this match
    candidates = (
        db.query(Player)
        .join(PlayerMatchStats, Player.id == PlayerMatchStats.player_id)
        .filter(PlayerMatchStats.match_id == match_id)
        .all()
    )

    best_player = None
    best_score = 0.0

    for player in candidates:
        norm_player = normalize_name(player.name)
        score = similarity(norm_target, norm_player)

        if score > best_score:
            best_score = score
            best_player = player

    if best_score >= threshold:
        return best_player

    return None
