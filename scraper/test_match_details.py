from transfermarkt.match_details import scrape_match_details

match_url = "https://www.transfermarkt.com/venezia-fc_uc-sampdoria/index/spielbericht/4692324"

match = scrape_match_details(match_url)

print(match)
