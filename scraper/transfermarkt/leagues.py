from scraper.playwright_driver import get_browser
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

def scrape_teams_from_league(league_url):
    playwright, browser, context, page = get_browser()

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

                teams.append({
                    "name": team_name,
                    "url": "https://www.transfermarkt.com" + team_url
                })
            except Exception:
                continue

    except PlaywrightTimeoutError:
        print("Timeout while loading league page")

    browser.close()
    playwright.stop()

    return teams
