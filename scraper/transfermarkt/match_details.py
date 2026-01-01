from scraper.playwright_driver import get_browser
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import re

def extract_match_id(match_url):
    # Transfermarkt match URLs contain /spielbericht/index/spielbericht/{id}
    match = re.search(r"/spielbericht/(\d+)", match_url)
    return match.group(1) if match else None


def scrape_match_details(match_url):
    playwright, browser, context, page = get_browser()

    page.goto(match_url, timeout=60000)

    match_data = {}

    try:
        # Wait for the match header to load
        page.wait_for_selector("div.row", timeout=20000)

        # Extract match ID
        match_id = extract_match_id(match_url)

        # Home team
        home_team_el = page.query_selector("div.sb-team.sb-heim a:nth-child(2)")
        home_team = home_team_el.inner_text().strip() if home_team_el else None

        # Away team
        away_team_el = page.query_selector("div.sb-team.sb-gast a:nth-child(2)")
        away_team = away_team_el.inner_text().strip() if away_team_el else None

        # Score
        score_el = page.query_selector(".sb-endstand")
        score_text = score_el.inner_text().strip() if score_el else None

        home_goals, away_goals = None, None
        if score_text and ":" in score_text:
            parts = score_text.split(":")
            home_goals = int(parts[0].strip())
            away_goals = int(parts[1].split("\n(")[0].strip())

        # Date
        date_el = page.query_selector(".sb-datum.hide-for-small a:nth-child(2)")
        date = date_el.inner_text().strip() if date_el else None

        # Competition
        comp_el = page.query_selector(".direct-headline a")
        competition = comp_el.inner_text().strip() if comp_el else None

        match_data = {
            "match_id": match_id,
            "date": date,
            "home_team": home_team,
            "away_team": away_team,
            "home_goals": home_goals,
            "away_goals": away_goals,
            "competition": competition,
            "match_url": match_url
        }

    except PlaywrightTimeoutError:
        print("Timeout while loading match page")

    browser.close()
    playwright.stop()

    return match_data
