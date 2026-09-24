# this module uses BeautifulSoup to parse the simulated HTML review pages - it extracts the average rating and review count from the specific <span> IDs we defined in mock server
import requests
from bs4 import BeautifulSoup
from config import SCRAPER_BASE_URL, REQUEST_TIMEOUT

def scrape_product_reviews(product_id: int) -> tuple[float, int]:
    url = f"{SCRAPER_BASE_URL}/{product_id}"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            return 0.0,0

        soup = BeautifulSoup(response.text, "html.parser")
        score_elem = soup.find("span", id="avg-score")
        count_elem = soup.find("span", id="review-count")

        avg_score = float(score_elem.text) if score_elem else 0.0
        review_count = int(count_elem.text) if count_elem else 0

        return avg_score, review_count
    except Exception as err:
        print(f"[Scraper Error] Product {product_id}: {err}")
        return 0.0,0