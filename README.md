# Product Aggregator

A local Python data pipeline that collects product data and review information, analyzes the results, and generates a market research report.

The project uses a mock HTTP server, so it can be run and tested without an external API.

## What It Does

- Fetches a product catalog from the mock API.
- Retrieves rating and review-count data for each product.
- Supports threaded and asynchronous execution modes.
- Filters out products with no reviews.
- Calculates average prices by category.
- Identifies the five highest-rated products.
- Prints a summary and saves the results to `report.json`.

## Requirements

- Python 3.9 or newer
- `pip`

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

Start the mock server in one terminal:

```bash
python3 mock_server.py
```

Run the aggregator in a second terminal. Threaded mode is the default:

```bash
python3 main.py --mode threads
```

To use the asynchronous implementation:

```bash
python3 main.py --mode async
```

The optional `--profile` flag prints `cProfile` performance information:

```bash
python3 main.py --mode async --profile
```

The final report is printed to the terminal and written to `report.json`.

## Project Structure

| File | Responsibility |
| --- | --- |
| `main.py` | Coordinates the threaded and async pipelines. |
| `mock_server.py` | Serves local product and review data. |
| `api_fetcher.py` | Fetches the product catalog. |
| `scraper.py` | Parses review pages with Beautiful Soup. |
| `data_models.py` | Defines the memory-efficient `Product` model. |
| `analyzer.py` | Filters, aggregates, and ranks products. |
| `reporter.py` | Prints and writes the final report. |
| `config.py` | Stores URLs and request timeout settings. |
| `report.json` | Example/generated report output. |

## Configuration

By default, the application connects to the local mock server:

```text
API_BASE_URL=http://localhost:8000/api/products
SCRAPER_BASE_URL=http://localhost:8000/reviews
```

These values and the request timeout can be overridden with environment variables:

```bash
API_BASE_URL="http://localhost:8000/api/products" \
SCRAPER_BASE_URL="http://localhost:8000/reviews" \
python3 main.py --mode async
```

## Documentation

- [`for_group/how.md`](for_group/how.md) explains the project history, debugging lessons, and code flow.
- [`for_group/TEAM_GUIDE.md`](for_group/TEAM_GUIDE.md) provides a beginner-friendly team walkthrough.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).