from transfermarkt.players import scrape_players_from_team
from transfermarkt.player_match_stats import scrape_player_match_stats
from transfermarkt.match_details import scrape_match_details

def test_player_matches(profile_url):
    print(f"\n=== Testing player: {profile_url} ===")

    # 1. Scrape player match stats (returns player-specific stats + match_url)
    player_stats = scrape_player_match_stats(profile_url)

    print(f"\nFound {len(player_stats)} match entries for this player.\n")

    # 2. Collect unique match URLs
    match_urls = set()
    for entry in player_stats:
        if "match_url" in entry and entry["match_url"]:
            match_urls.add(entry["match_url"])

    print(f"Unique matches found: {len(match_urls)}\n")

    # 3. Scrape match details for each match
    for url in list(match_urls)[:5]:  # limit to 5 for testing
        print(f"\n--- Scraping match: {url} ---")
        match_info = scrape_match_details(url)
        print(match_info)


if __name__ == "__main__":
    # Example: Daniel Fila
    test_player_matches("https://www.transfermarkt.com/daniel-fila/leistungsdatendetails/spieler/666268/wettbewerb/IT2/saison/2025")
