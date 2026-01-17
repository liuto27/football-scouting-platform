from scraper.playwright_driver import get_browser
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


def scrape_diretta_player_ratings(diretta_url: str):
    """
    Returns list of dicts:
    --- in the future way more statistics can be retrieved ----
    {
        "player_name": "...",
        "rating": 6.5
    }
    """
    playwright, browser, context, page = get_browser()
    print(f"Scraping Diretta ratings: {diretta_url}")
    page.goto(diretta_url, timeout=60000)

    ratings = []

    try:
        # You may need to adjust selectors based on the real DOM.
        # The idea: there are two tables, one per team, listing players and ratings.
        page.wait_for_selector("table", timeout=20000)

        rows = page.query_selector_all("table tbody tr")
        for row in rows:
            name_el = row.query_selector("td:nth-child(1) figure figcaption span:nth-child(1) div")
            rating_el = row.query_selector("td:nth-child(2) div span")
            if not name_el or not rating_el:
                continue

            name = name_el.inner_text().strip()
            rating_text = rating_el.inner_text().strip()

            try:
                rating = float(rating_text.replace(",", "."))
            except ValueError:
                continue

            ratings.append({
                "player_name": name,
                "rating": rating,
            })

    except PlaywrightTimeoutError:
        print("Timeout while loading Diretta page")

    browser.close()
    playwright.stop()

    return ratings

# FOR TESTING
# rtgs=scrape_diretta_player_ratings("https://www.diretta.it/partita/calcio/juve-stabia-hKSfjtsQ/pescara-WW0i6v4C/riassunto/statistiche-giocatore/principali/?mid=tEUugwW1")
# print(rtgs)