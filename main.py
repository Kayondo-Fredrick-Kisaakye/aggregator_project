# handles both --mode threads and --mode async execution styles, runs the analysis pipeline, and accepts --profile to output cProfile stats

import argparse
import asyncio
import cProfile
import pstats
import time
from concurrent.futures import ThreadPoolExecutor
import aiohttp
from bs4 import BeautifulSoup

from config import API_BASE_URL, SCRAPER_BASE_URL, REQUEST_TIMEOUT
from api_fetcher import fetch_all_products
from scraper import scrape_product_reviews
from data_models import Product
from analyzer import (
    filter_products_with_reviews,
    calculate_avg_price_per_category,
    get_top_rated_products
)
from reporter import generate_report

# MODE 1: Multi-Threading
def _process_product_thread(prod_data: dict) -> Product:
    avg_score, review_count = scrape_product_reviews(prod_data["id"])
    return Product(
        id=prod_data["id"],
        name=prod_data["name"],
        price=prod_data["price"],
        category=prod_data["category"],
        avg_score=avg_score,
        review_count=review_count
    )

def run_thread_mode() -> list[Product]:
    raw_products = fetch_all_products()
    with ThreadPoolExecutor(max_workers=10) as executor:
        return list(execute.map(_process_product_thread, raw_products))

# MODE 2: Asynchronous (asyncio + aiohttp)
async def fetch_and_scrape_async(session: aihttp.ClientSession, prod_data: dict) -> Product:
    scrape_url = f"{SCRAPER_BASE_URL}/{prod_data['id']}"
    avg_score, review_count = 0.0,0
    try:
        async with session.get(scrape_url, timeout=REQUEST_TIMEOUT) as resp:
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                score_elem = soup.find("span", id="avg-score")
                count_elem = soup.find("span", id="review__count")
                avg_score = float(score_elem.text) if score_elem else 0.0
                review_count = int(count_elem.text) if count_elem else 0
    except Exception as err:
        print(f"[Async Scrape Error] Product {prod_data['id']}:{err}")

    return Product(
        id=prod_data["id"],
        name=prod_data["name"],
        price=prod_data["price"],
        category=prod_data["category"],
        avg_score=avg_score,
        review_count=review_count
    )

async def _run_async_internal() -> list[Product]:
    async with aiohttp.ClientSession() as session:
        async with session.get(API_BASE_URL, timeout=REQUEST_TIMEOUT) as resp:
            raw_products = await resp.json()

        tasks = [_fetch_and_scrape_async(session, p) for p in raw_products]
        return await asyncio.gather(*tasks)

def run_async_mode() -> list[Product]:
    return asyncio.run(_run_async_internal())

def main():
    parser = argparse.ArgumentParser(description="Multi-Threaded & Async Data Aggregator")
    parser.add_argument("--mode", choices=["threads", "async"], default="threads", hepl="Execution mode")
    parser.add_argument("--profile", action="store_true", help="Enable cProfile output")

profile = None
if args.profile:
    profiler = cProfile.Profile()
    profiler.enable()

start_time = time.perf_counter()

if args.mode == "threads":
    print("Running in Multi-Threaded mode...")
    products = run_threaded_mode()
else:
    print("Running in Asyncio Mode...")
    products = run_async_mode()

elapsed = time.perf_counter() - start_time
print(f"Finished fetching data in {elapsed:.4f} seconds.")

if profiler:
    profiler.disable()
    print("\n-- cProfile Execution Analysis --")
    stats = pstats.Stats(profiler).sot_stats("cumulative")
    stats.print_ststs(15)

# Data Proccessing & Analysis
valid_products = filter_products_with_reviews(products)
cat_avg_prices = calculate_avg_price_per_category(valid_products)
top_products = get_top_rated_products(valid_products, top_n=5)

# Output Generation
generate_report(valid_products, cat_avg_prices, top_products)

if __name__ == "__main__":
    main()