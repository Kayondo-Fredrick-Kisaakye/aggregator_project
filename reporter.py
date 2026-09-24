# formats and prints summary metrics to the console and writes the structured output to report.json
import json
from data_models import Product

def generate_report(
        products:list[Product],
        avg_price_per_cat: dict[str, float],
        top_products: list[Product],
        output_filepath: str = "report.json"
)-> dict:
    report_data =  {
        "total_products_analyzed": len(products),
        "average_price_per_category": avg_price_per_cat,
        "top_5_highest_rated": [p.to_dict() for p in top_products]
    }

    print("\n" + "=" * 45)
    print("     MARKET RESEARCH AGGREGATOR REPORT       ")
    print("=" * 45)
    print(f"Total Reviewed Products: {report_data['total_products_analyzed']}")
    print("\nAverage Price per Category:")
    for cat, price in avg_price_per_cat.items():
        print(f" -{cat:<15}: UGX{price:.2f}")

    print("\nTop 5 Highest-Rated Products:")
    for idx, p in enumerate(top_products, start=1):
        print(f" {idx}. {p.name:<20} | Rating: {p.avg_score}/5.0 ({p.review_count} reviews) | UGX{p.price:.2f}")
    print("=" * 45 + "\n")

    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    print(f"[+] Output writen to {output_filepath}")
    return report_data