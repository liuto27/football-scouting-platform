from scraper.playwright_driver import get_browser
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import re


def extract_player_id(profile_url):
    match = re.search(r"/spieler/(\d+)", profile_url)
    return match.group(1) if match else None


def scrape_players_from_team(team_url):
    playwright, browser, context, page = get_browser()

    print(f"Scraping players from: {team_url}")
    page.goto(team_url, timeout=60000)

    players = []

    try:
        page.wait_for_selector("table.items", timeout=20000)

        # Only real player rows
        rows = page.query_selector_all("table.items tbody tr.odd, table.items tbody tr.even")

        for row in rows:
            try:
                # Player name + profile URL
                link = row.query_selector("td.hauptlink a")
                if not link:
                    continue

                name = link.inner_text().strip()
                player_url = "https://www.transfermarkt.com" + link.get_attribute("href")
                player_id = extract_player_id(player_url)

                # Position
                pos_el = row.query_selector("td:nth-child(2) table tr:nth-child(2) td")
                position = pos_el.inner_text().strip() if pos_el else None

                # Birthdate
                birth_el = row.query_selector("td.zentriert:nth-child(3)")
                birthdate = birth_el.inner_text().strip()[:10] if birth_el else None

                # Nationality
                nat_el = row.query_selector("td.zentriert:nth-child(4) img")
                nationality = nat_el.get_attribute("title") if nat_el else None

                players.append({
                    "id": player_id,
                    "name": name,
                    "player_url": player_url,
                    "position": position,
                    "nationality": nationality,
                    "birthdate": birthdate
                })

            except Exception:
                continue

    except PlaywrightTimeoutError:
        print("Timeout while loading team page")

    browser.close()
    playwright.stop()

    return players
