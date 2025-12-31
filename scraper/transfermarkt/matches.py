import re
from scraper.playwright_driver import get_browser

def extract_player_id(profile_url):
    match = re.search(r"/spieler/(\d+)", profile_url)
    return match.group(1) if match else None


def scrape_player_match_stats(profile_url):
    player_id = extract_player_id(profile_url)
    if not player_id:
        print("Could not extract player ID")
        return []

    stats_url = (
        f"https://www.transfermarkt.com/leistungsdatendetails/spieler/{player_id}"
        f"/saison/0/verein/0/liga/0/wettbewerb/0/pos/0/trainer_id/0/plus/1"
    )

    playwright, browser, context, page = get_browser()
    print(f"Scraping match stats: {stats_url}")
    page.goto(stats_url, timeout=60000)

    matches = []

    try:
        page.wait_for_selector("table.items", timeout=20000)
        rows = page.query_selector_all("table.items tbody tr")

        for row in rows:
            try:
                # Skip header rows
                if "bg_blau_20" in (row.get_attribute("class") or ""):
                    continue

                date_el = row.query_selector("td:nth-child(2)")
                date = date_el.inner_text().strip() if date_el else None

                competition_el = row.query_selector("td:nth-child(3) a")
                competition = competition_el.inner_text().strip() if competition_el else None

                opponent_el = row.query_selector("td:nth-child(5) a")
                opponent = opponent_el.inner_text().strip() if opponent_el else None

                result_el = row.query_selector("td:nth-child(6) a")
                result = result_el.inner_text().strip() if result_el else None

                minutes_el = row.query_selector("td:nth-child(8)")
                minutes = minutes_el.inner_text().strip() if minutes_el else None

                goals_el = row.query_selector("td:nth-child(9)")
                goals = goals_el.inner_text().strip() if goals_el else None

                assists_el = row.query_selector("td:nth-child(10)")
                assists = assists_el.inner_text().strip() if assists_el else None

                yellow_el = row.query_selector("td:nth-child(11)")
                yellow = yellow_el.inner_text().strip() if yellow_el else None

                red_el = row.query_selector("td:nth-child(12)")
                red = red_el.inner_text().strip() if red_el else None

                matches.append({
                    "date": date,
                    "competition": competition,
                    "opponent": opponent,
                    "result": result,
                    "minutes": minutes,
                    "goals": goals,
                    "assists": assists,
                    "yellow": yellow,
                    "red": red
                })

            except Exception:
                continue

    except Exception as e:
        print("Error:", e)

    browser.close()
    playwright.stop()

    return matches
