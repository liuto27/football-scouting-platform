from transfermarkt.teams import scrape_teams_from_league

url = "https://www.transfermarkt.com/serie-b/startseite/wettbewerb/IT2"

teams = scrape_teams_from_league(url)

for s in teams:
    print(s)
