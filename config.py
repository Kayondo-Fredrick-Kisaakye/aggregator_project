# this file holds our urls, by default to localhost - we ensure the entire app can be built and tested offline
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/products")
SCRAPER_BASE_URL = os.getenv("SCRAPER_BASE_URL", "http://localhost:8000/reviews")
REQUEST_TIMEOUT = 5 # are seconds