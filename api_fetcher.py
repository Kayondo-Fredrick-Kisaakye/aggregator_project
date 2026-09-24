# this one fetches the raw product data from our mock API using the requests library - it uses lru_cache to remember recent requests
# preventing duplicate network calls for the same item

from functools import lru_cache
import requests
from config import API_BASE_URL, REQUEST_TIMEOUT

@lru_cache(maxsize=128)
def fetch_product_details_cached(product_id: int) -> dict:
    url = f"{API_BASE_URL}/{product_id}"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"[API Error] Failed to fetch product {product_id}: {err}")
    return{}

def fetch_all_products() ->  list[dict]:
    try:
        response = requests.get(API_BASE_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"[API Error] Failed to fetch product catalog: {err}")
        return[]