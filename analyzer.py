# this module fullfills the functional programming requirement
# - it uses map, filter, and reduce to discard products with zero reviews,
# calulate the average price for each category and find top rated items
from functools import reduce
from data_models import Product

def filter_products_with_reviews(products: list[Product]) -> list[Product]:
    return list(filter(lambda p: p.review_count > 0, products))

def calculate_avg_price_per_category(products: list[Product]) -> dict[str, float]:
    categories = set(map(lambda p: p.category, products))
    avg_prices = {}

    for category in categories:
        cat_items = list(filter(lambda p: p.category == category, products))
        if cat_items:
            total_price = reduce(lambda acc, p: acc + p.price, cat_items, 0.0)
            avg_prices[category] = round(total_price/len(cat_items), 2)

    return avg_prices

def get_top_rated_products(products: list[Product], top_n: int = 5) -> list[Product]:
    return sorted(products, key=lambda p: p.avg_score, reverse=True)[:top_n]