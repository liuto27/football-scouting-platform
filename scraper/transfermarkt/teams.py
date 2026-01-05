from scraper.playwright_driver import get_browser
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import re


def extract_league_id(league_url):
    match = re.search(r"/wettbewerb/(\d+)", league_url)
    return match.group(1) if match else None


def extract_team_id(team_url):
    team = re.search(r"/verein/(\d+)", team_url)
    return team.group(1) if team else None


def scrape_teams_from_league(league_url):
    playwright, browser, context, page = get_browser()
    league_id = extract_league_id(league_url)

    print(f"Scraping league: {league_url}")
    page.goto(league_url, timeout=60000)

    teams = []

    try:
        # Wait for the table to load
        page.wait_for_selector("table.items", timeout=20000)

        rows = page.query_selector_all("table.items tbody tr")

        for row in rows:
            try:
                link = row.query_selector("td:nth-child(2) a")
                if not link:
                    continue

                team_name = link.inner_text().strip()
                team_url = link.get_attribute("href")
                team_id = extract_team_id(team_url)

                teams.append({
                    "id": team_id,
                    "name": team_name,
                    "team_url": team_url,
                    "league_url": league_url,
                    "league_id": league_id
                })
            except Exception:
                continue

    except PlaywrightTimeoutError:
        print("Timeout while loading league page")

    browser.close()
    playwright.stop()

    return teams
