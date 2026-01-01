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
        f"https://www.transfermarkt.com/{player_id}/leistungsdatendetails/spieler/{player_id}"
        f"/verein/0/liga/0/wettbewerb/IT2/pos/0/trainer_id/0"
    )

    playwright, browser, context, page = get_browser()
    print(f"Scraping match stats: {stats_url}")
    page.goto(stats_url, timeout=60000)

    player_match = []

    try:
        page.wait_for_selector("table.items", timeout=20000)
        rows = page.query_selector_all("div.responsive-table table tbody tr")

        for row in rows:
            counter = 0
            try:
                # Skip header rows
                if "bg_blau_20" in (row.get_attribute("class") or ""):
                    continue

                # Check if 5th td has a span
                opponent_td = row.query_selector("td:nth-child(5)")
                span = opponent_td.query_selector("span") if opponent_td else None
                if span is not None:
                    counter += 1

                minutes_el = row.query_selector(f"td:nth-child({14+counter})")
                minutes = minutes_el.inner_text().strip() if minutes_el else None

                # stop if minutes is None, as the player hasn't played
                if minutes is None:
                    continue

                link = row.query_selector(f"td:nth-child({7 + counter}) a")
                if not link:
                    continue
                match_url = "https://www.transfermarkt.com" + link.get_attribute("href")



                goals_el = row.query_selector(f"td:nth-child({9+counter})")
                goals = goals_el.inner_text().strip() if goals_el else None

                assists_el = row.query_selector(f"td:nth-child({10+counter})")
                assists = assists_el.inner_text().strip() if assists_el else None

                yellow_el = row.query_selector(f"td:nth-child({11 + counter})")
                yellow = False
                if yellow_el:
                    text = yellow_el.inner_text().strip()
                    if text not in ("", "-", None):
                        yellow = True

                second_yellow_el = row.query_selector(f"td:nth-child({12+counter})")
                second_yellow = False
                if second_yellow_el:
                    text = second_yellow_el.inner_text().strip()
                    if text not in ("", "-", None):
                        second_yellow = True

                red_el = row.query_selector(f"td:nth-child({13+counter})")
                red = False
                if red_el:
                    text = red_el.inner_text().strip()
                    if text not in ("", "-", None):
                        red = True

                player_match.append({
                    "minutes": minutes,
                    "match_url": match_url,
                    "goals": goals,
                    "assists": assists,
                    "yellow": yellow,
                    "second_yellow": second_yellow,
                    "red": red
                })

            except Exception:
                continue

    except Exception as e:
        print("Error:", e)

    browser.close()
    playwright.stop()

    return player_match
