from transfermarkt.players import scrape_players_from_team
from transfermarkt.matches import scrape_player_match_stats

team_url = "https://www.transfermarkt.com/venezia-fc/startseite/verein/607/saison_id/2025"

players = scrape_players_from_team(team_url)
first_player = players[-8]

print("Testing player:", first_player["name"])
stats = scrape_player_match_stats(first_player["profile_url"])

for s in stats:
    print(s)
