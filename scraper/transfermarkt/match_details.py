from scraper.playwright_driver import get_browser
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import re
from datetime import datetime


def extract_match_id(match_url):
    # Transfermarkt match URLs contain /spielbericht/index/spielbericht/{id}
    match = re.search(r"/spielbericht/(\d+)", match_url)
    return match.group(1) if match else None


def extract_team_id(team_url):
    team = re.search(r"/startseite/verein/(\d+)", team_url)
    return team.group(1) if team else None


def extract_league_id(league_url):
    league = re.search(r"/wettbewerb/(\d+)", league_url)
    return league.group(1) if league else None


def parse_match_date(raw):
    if not raw:
        return None
    return datetime.strptime(raw, "%a, %d/%m/%y").date()


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
        home_team_url = "https://www.transfermarkt.com" + home_team_el.get_attribute("href")
        home_team_id = extract_team_id(home_team_url)

        # Away team
        away_team_el = page.query_selector("div.sb-team.sb-gast a:nth-child(2)")
        away_team = away_team_el.inner_text().strip() if away_team_el else None
        away_team_url = "https://www.transfermarkt.com" + away_team_el.get_attribute("href")
        away_team_id = extract_team_id(away_team_url)

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
        league = comp_el.inner_text().strip() if comp_el else None
        league_url = "https://www.transfermarkt.com" + comp_el.get_attribute("href")
        league_id = extract_league_id(league_url)

        match_data = {
            "id": match_id,
            "date": parse_match_date(date),
            "home_team_name": home_team,
            "away_team_name": away_team,
            "home_team_id": home_team_id,
            "away_team_id": away_team_id,
            "home_goals": home_goals,
            "away_goals": away_goals,
            "league_name": league,
            "league_id": league_id,
            "match_url": match_url
        }

    except PlaywrightTimeoutError:
        print("Timeout while loading match page")

    browser.close()
    playwright.stop()

    return match_data
